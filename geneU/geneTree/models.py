from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo, RelationshipFrom, Relationship,
    ZeroOrOne)
from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate
from uuid import uuid4
from neomodel import db

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
        self.birth_date_begin = args.pop('birth_date_begin')
        self.birth_date_end = args.pop('birth_date_end')
        self.death_date_begin = args.pop('death_date_begin')
        self.death_date_end = args.pop('death_date_end')
        self.son_of = args.pop('son_of')
        self.sons = args.pop('sons')
        self.adopted = args.pop('adopted')
        self.adopted_by = args.pop('adopted_by')
        self.married = args.pop('married')
        self.divorced = args.pop('divorced')
        self.born_in = args.pop('born_in')
        self.death_in = args.pop('death_in')
        self.lived_in = args.pop('lived_in')

        super(Person, self).__init__(self, **args)

    def __get_person(self, per):
            # return list(Person.nodes.filter(id=per))[0]
            return Person.nodes.get(id=per)

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

    def __set_death_date_begin(self, begin):
        for dd in self.death_date_begin.all():
            self.death_date_begin.disconnect(dd)
        beg = NodeDate(begin).save()
        self.death_date_begin.connect(beg)

    def __set_death_date_end(self, end):
        for dd in self.death_date_end.all():
            self.death_date_end.disconnect(dd)
        nd = NodeDate(end).save()
        self.death_date_end.connect(nd)

    def __set_birth_date_begin(self, begin):
        for dd in self.birth_date_begin.all():
            self.birth_date_begin.disconnect(dd)
        beg = NodeDate(begin).save()
        self.birth_date_begin.connect(beg)

    def __set_birth_date_end(self, end):
        for dd in self.birth_date_end.all():
            self.birth_date_end.disconnect(dd)
        nd = NodeDate(end).save()
        self.birth_date_end.connect(nd)

    def __add_sons(self, sons):
        for son_id in sons:
            son = Person.nodes.filter(id=son_id)
            self.sons.connect(son)

    def __add_son_of(self, son_of):
        for idd in son_of:
            son_of = Person.nodes.filter(id=idd)
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
            p = Person.nodes.filter(id=ad)
            self.adopted.connect(p)

    def __add_adopted_by(self, adopted_by):
        for fath in adopted_by:
            p = Person.nodes.filter(id=fath)
            self.adopted_by.connect(p)

    def save(self):
        super(Person, self).save(self)
        if self.birth_date_begin:
            self.__set_birth_date_begin(self.birth_date_begin)
        if self.birth_date_end:
            self.__set_birth_date_end(self.birth_date_end)
        if self.death_date_begin:
            self.__set_death_date_begin(self.death_date_begin)
        if self.birth_date_end:
            self.__set_birth_date_end(self.birth_date_end)
        if self.born_in:
            self.__set_born_in(self.born_in)
        if self.death_in:
            self.__set_death_in(self.death_in)
        if self.sons:
            self.__add_sons(self.sons)
        if self.son_of:
            self.__add_sons_of(self.son_of)
        if self.lived_in:
            self.__add_lived_in(self.lived_in)
        if self.divorced:
            self.__add_divorced(self.divorced)
        if self.married:
            self.__add_married(self.married)
        if self.adopted:
            self.__add_married(self.adopted)
        if self.adopted_by:
            self.__add_adopted_by(self.adopted_by)
        return self

    @db.transaction
    def add_divorced(self, per):
        self.__add_divorced(per)

    @db.transaction
    def add_married(self, per):
        self.__add_married(per)

    @db.transaction
    def set_birth_date_begin(self, begin):
        self.__set_birth_date_begin(begin)

    @db.transaction
    def set_birth_date_end(self, end):
        self.__set_birth_date_end(end)

    @db.transaction
    def set_death_date_begin(self, begin):
        self.__set_death_date_begin(begin)

    @db.transaction
    def set_death_date_end(self, end):
        self.__set_death_date_end(end)

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
