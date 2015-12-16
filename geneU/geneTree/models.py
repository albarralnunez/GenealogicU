from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo, RelationshipFrom, Relationship,
    ZeroOrOne)
from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate
from uuid import uuid4
from neomodel import db
from datetime import datetime
# from django.core.exceptions.entry import DoesNotExist


class Person(StructuredNode):
    id = StringProperty(unique_index=True, default=uuid4)
    name = StringProperty(required=True)
    surname = StringProperty(index=True)
    second_surname = StringProperty(index=True)
    genere = StringProperty(choices=(('M', 1), ('W', 2)))

    birth_date_begin = RelationshipTo(
        Day, 'BIRTH_DATE_BEGIN', cardinality=ZeroOrOne)
    birth_date_end = RelationshipTo(
        Day, 'BIRTH_DATE_END', cardinality=ZeroOrOne)
    death_date_begin = RelationshipTo(
        Day, 'DEATH_DATE_BEGIN', cardinality=ZeroOrOne)
    death_date_end = RelationshipTo(
        Day, 'DEATH_DATE_END', cardinality=ZeroOrOne)

    married = Relationship('Person', 'MARRIED')
    divorced = Relationship('Person', 'DIVORCED')
    sons = RelationshipTo('Person', 'SON')
    son_of = RelationshipFrom('Person', 'SON')
    adopted = RelationshipTo('Person', 'ADOPTED')
    adopted_by = RelationshipFrom('Person', 'ADOPTED')

    born_in = RelationshipTo(
        AddressComponent, 'BORN_IN', cardinality=ZeroOrOne)
    death_in = RelationshipTo(
        AddressComponent, 'DEATH_IN', cardinality=ZeroOrOne)
    lived_in = RelationshipTo(
        AddressComponent, 'LIVED_IN')

    def __init__(self, **args):
        self.rel_birth_date = (None, None)
        self.rel_death_date = (None, None)
        self.rel_son_of = None
        self.rel_sons = None
        self.rel_adopted = None
        self.rel_adopted_by = None
        self.rel_married = None
        self.rel_divorced = None
        self.rel_born_in = None
        self.rel_death_in = None
        self.rel_lived_in = None
        if 'birth_date' in args:
            self.rel_birth_date = args.pop('birth_date')
        if 'death_date' in args:
            self.rel_death_date = args.pop('death_date')
        if 'son_of' in args:
            self.rel_son_of = args.pop('son_of')
        if 'sons' in args:
            self.rel_sons = args.pop('sons')
        if 'adopted' in args:
            self.rel_adopted = args.pop('adopted')
        if 'adopted_by' in args:
            self.rel_adopted_by = args.pop('adopted_by')
        if 'married' in args:
            self.rel_married = args.pop('married')
        if 'divorced' in args:
            self.rel_divorced = args.pop('divorced')
        if 'born_in' in args:
            self.rel_born_in = args.pop('born_in')
        if 'death_in' in args:
            self.rel_death_in = args.pop('death_in')
        if 'lived_in' in args:
            self.rel_lived_in = args.pop('lived_in')

        super(Person, self).__init__(self, **args)

    def __get_person(self, id):
            # return list(Person.nodes.filter(id=per))[0]
            return Person.nodes.get(id=id)

    def __add_divorced(self, per):
        for idd in per:
            p = self.__get_person(idd)
            if (self.married.is_connected(p)):
                self.married.disconnect(p)
            self.divorced.connect(p)

    def __add_married(self, per):
        for idd in per:
            p = self.__get_person(idd)
            if (self.divorced.is_connected(p)):
                self.divorced.disconnect(p)
            self.married.connect(p)

    def __set_death_date(self, date):
        begin, end = date
        if begin and end and end < begin:
            raise ValueError(
                'Start date must be less or equal to the end date')
        if begin:
            for dd in self.death_date_begin.all():
                self.death_date_begin.disconnect(dd)
            beg = NodeDate(begin).save()
            self.death_date_begin.connect(beg)
        if end:
            for dd in self.death_date_end.all():
                self.death_date_end.disconnect(dd)
            en = NodeDate(end).save()
            self.death_date_end.connect(en)

    def __set_birth_date(self, date):
        begin, end = date
        if begin and end and end < begin:
            raise ValueError(
                'Start date must be less or equal to the end date')
        if begin:
            for dd in self.birth_date_begin.all():
                self.birth_date_begin.disconnect(dd)
            beg = NodeDate(begin).save()
            self.birth_date_begin.connect(beg)
        if end:
            for dd in self.death_date_end.all():
                self.death_date_end.disconnect(dd)
            en = NodeDate(end).save()
            self.death_date_end.connect(en)

    def __add_sons(self, sons):
        for son_id in sons:
            son = self.__get_person(id=son_id)
            self.sons.connect(son)

    def __add_son_of(self, son_of):
        for idd in son_of:
            son_of = self.__get_person(id=idd)
            self.son_of.connect(son_of)

    def __set_born_in(self, born_in):
        for node in self.born_in.all():
            self.born_in.disconnect(node)
        dd = Location(address_components=born_in).save()
        self.born_in.connect(dd)

    def __set_death_in(self, death_in):
        for node in self.death_in.all():
            self.death_in.disconnect(node)
        dd = Location(address_components=death_in).save()
        self.death_in.connect(dd)

    def __add_lived_in(self, lived_in):
        for loc in lived_in:
            lived_in = Location(address_components=loc).save()
            self.lived_in.connect(lived_in)

    def __add_adopted(self, adopted):
        for ad in adopted:
            p = self.__get_person(id=ad)
            self.adopted.connect(p)

    def __add_adopted_by(self, adopted_by):
        for fath in adopted_by:
            p = self.__get_person(id=fath)
            self.adopted_by.connect(p)

    def __get_birth_date_begin(self):
        a = list(self.birth_date_begin.all())
        return None if not a else datetime.strptime(a[0].id, "%Y-%m-%d")

    def __get_birth_date_end(self):
        a = list(self.birth_date_end.all())
        return None if not a else datetime.strptime(a[0].id, "%Y-%m-%d")

    def __get_death_date_begin(self):
        a = list(self.death_date_begin.all())
        return None if not a else datetime.strptime(a[0].id, "%Y-%m-%d")

    def __get_death_date_end(self):
        a = list(self.death_date_end.all())
        return None if not a else datetime.strptime(a[0].id, "%Y-%m-%d")

    @db.transaction
    def complete_save(self):
        self.save()
        if any(self.rel_birth_date):
            self.__set_birth_date(self.rel_birth_date)
        if any(self.rel_death_date):
            self.__set_death_date(self.rel_death_date)
        if self.rel_born_in:
            self.__set_born_in(self.rel_born_in)
        if self.rel_death_in:
            self.__set_death_in(self.rel_death_in)
        if self.rel_sons:
            self.__add_sons(self.rel_sons)
        if self.rel_son_of:
            self.__add_son_of(self.rel_son_of)
        if self.rel_lived_in:
            self.__add_lived_in(self.rel_lived_in)
        if self.rel_divorced:
            self.__add_divorced(self.rel_divorced)
        if self.rel_married:
            self.__add_married(self.rel_married)
        if self.rel_adopted:
            self.__add_married(self.rel_adopted)
        if self.rel_adopted_by:
            self.__add_adopted_by(self.rel_adopted_by)
        return self

    @db.transaction
    def add_divorced(self, per):
        self.__add_divorced(per)

    @db.transaction
    def add_married(self, per):
        self.__add_married(per)

    @db.transaction
    def set_birth_date(self, date):
        begin, end = date
        self.__set_birth_date(begin, end)

    @db.transaction
    def set_death_date(self, date):
        begin, end = date
        self.__set_death_date(begin, end)

    @db.transaction
    def add_sons(self, sons):
        self.__add_sons(sons)

    @db.transaction
    def add_son_of(self, son_of):
        self.__add_son_of(son_of)

    @db.transaction
    def set_born_in(self, born_in):
        self.__set_born_in(born_in)

    @db.transaction
    def set_death_in(self, death_in):
        self.__set_death_in(death_in)

    @db.transaction
    def add_lived_in(self, lived_in):
        self.__add_lived_in(lived_in)

    @db.transaction
    def add_adopted(self, adopted):
        self.__add_adopted(adopted)

    @db.transaction
    def add_adopted_by(self, adopted_by):
        self.__add_adopted_by(adopted_by)

    @db.transaction
    def update_person(self, data):
        self.name = data.get('name', self.name)
        self.surname = data.get('surname', self.surname)
        self.second_surname = data.get('second_surname', self.second_surname)
        self.genere = data.get('genere', self.genere)
        self.rel_birth_date = data.get('birth_date')
        self.rel_death_date = data.get('death_date')
        self.rel_sons = data.get('sons')
        self.rel_son_of = data.get('son_of')
        self.rel_born_in = data.get('born_in')
        self.rel_death_in = data.get('death_in')
        self.rel_lived_in = data.get('lived_in')
        self.rel_divorced = data.get('divorced')
        self.rel_married = data.get('married')
        self.rel_adopted = data.get('adopted')
        self.rel_adopted_by = data.get('adopted_by')

        if any(self.rel_birth_date):
            self.__set_birth_date(self.rel_birth_date)

        if any(self.rel_death_date):
            self.__set_death_date(self.rel_death_date)

        if self.rel_sons:
            self.__add_sons(self.rel_sons)
        if self.rel_son_of:
            self.__add_sons_of(self.rel_son_of)
        if self.rel_born_in:
            self.__set_born_in(self.rel_born_in)
        if self.rel_death_in:
            self.__set_death_in(self.rel_death_in)
        if self.rel_lived_in:
            self.__add_lived_in(self.rel_lived_in)
        if self.rel_divorced:
            self.__add_divorced(self.rel_divorced)
        if self.rel_married:
            self.__add_married(self.rel_married)
        if self.rel_adopted:
            self.__add_adopted(self.rel_adopted)
        if self.rel_adopted_by:
            self.__add_adopted_by(self.rel_adopted_by)

        self.refresh()

        return self
