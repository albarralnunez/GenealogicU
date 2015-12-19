from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo, RelationshipFrom, Relationship,
    ZeroOrOne)
from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate
from uuid import uuid4
import datetime
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

    def get_birth_date(self):
        return (
            self.__get_birth_date_begin().id,
            self.__get_birth_date_end().id
            )

    def get_death_date(self):
        return (
            self.__get_death_date_begin().id,
            self.__get_death_date_end().id
            )

    def get_lived_in(self):
        a = list(self.lived_in.all())
        return [x.addres for x in a]

    def get_born_in(self):
        a = list(self.birth_in.all())
        return None if not a else a[0].addres

    def get_death_in(self):
        a = list(self.death_in.all())
        return None if not a else a[0].addres

    def get_married(self):
        a = list(self.married.all())
        return [x.id for x in a]

    def get_divorced(self):
        a = list(self.divorced.all())
        return [x.id for x in a]

    def get_adopted(self):
        a = list(self.adopted.all())
        return [x.id for x in a]

    def get_adopted_by(self):
        a = list(self.adopted_by.all())
        return [x.id for x in a]

    def get_sons(self):
        a = list(self.sons.all())
        return [x.id for x in a]

    def get_son_of(self):
        a = list(self.son_of.all())
        return [x.id for x in a]

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

    def __set_relations(self):
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

    def complete_save(self):
        self.save()
        self.__set_relations()
        return self

    def add_divorced(self, per):
        self.__add_divorced(per)

    def add_married(self, per):
        self.__add_married(per)

    def set_birth_date(self, date):
        begin, end = date
        self.__set_birth_date(begin, end)

    def set_death_date(self, date):
        begin, end = date
        self.__set_death_date(begin, end)

    def add_sons(self, sons):
        self.__add_sons(sons)

    def add_son_of(self, son_of):
        self.__add_son_of(son_of)

    def set_born_in(self, born_in):
        self.__set_born_in(born_in)

    def set_death_in(self, death_in):
        self.__set_death_in(death_in)

    def add_lived_in(self, lived_in):
        self.__add_lived_in(lived_in)

    def add_adopted(self, adopted):
        self.__add_adopted(adopted)

    def add_adopted_by(self, adopted_by):
        self.__add_adopted_by(adopted_by)

    def update_person(self, **data):

        #  if 'name' not in data:
        #    data.append(self.name)
        print data.get('name')

        self.__set_relations()
        #self.save()
        return self
