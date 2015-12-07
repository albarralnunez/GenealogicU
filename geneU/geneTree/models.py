from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo, RelationshipFrom, Relationship,
    ZeroOrOne)
from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate
from uuid import uuid4


class Person(StructuredNode):
    id = StringProperty(unique_index=True, default=uuid4)
    name = StringProperty(required=True)
    surname = StringProperty(index=True)
    second_surname = StringProperty(index=True)
    genere = StringProperty(choices=(('M', 1), ('W', 2)))

    birth_date = RelationshipTo(Day, 'BIRTH_DATE')
    death_date = RelationshipTo(Day, 'DEATH_DATE')

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

    def add_divorced(self, per):
        for id in per:
            p = list(Person.node.filter(id=id))[0]
            if (self.married.is_connected(p)):
                self.married.disconnect(p)
            self.divorced.connect(p)

    def add_marryed(self, per):
        for id in per:
            p = list(Person.node.filter(id=id))[0]
            if (self.divorced.is_connected(p)):
                self.divorced.disconnect(p)
            self.married.connect(p)

    def set_death_date(self, date):
        for dd in self.death_date.all():
            self.death_date.disconnect(dd)
        dd = NodeDate(date).save()
        self.death_date.connect(dd)

    def set_birth_date(self, date):
        for dd in self.birth_date.all():
            self.birth_date.disconnect(dd)
        dd = NodeDate(date).save()
        self.birth_date.connect(dd)

    def add_sons(self, sons):
        for son_id in sons:
            son = Person.node.filter(id=son_id)
            self.sons.connect(son)

    def add_son_of(self, son_of):
        for id in son_of:
            son_of = Person.node.filter(id=id)
            self.son_of.connect(son_of)

    def set_born_in(self, born_in):
        for node in self.born_in.all():
            self.born_in.disconnect(node)
        dd = Location(address_components=born_in).save()
        self.born_in.connect(dd)

    def set_death_in(self, death_in):
        for node in self.death_in.all():
            self.death_in.disconnect(node)
        dd = Location(address_components=death_in).save()
        self.death_in.connect(dd)

    def add_lived_in(self, lived_in):
        for id in lived_in:
            lived_in = Location(address_components=lived_in).save()
            self.lived_in.connect(lived_in)

    def add_adopted(self, adopted):
        for id in adopted:
            p = Person.node.filter(id=id)
            self.adopted.connect(p)

    def add_adopted_by(self, adopted_by):
        for id in adopted_by:
            p = Person.node.filter(id=id)
            self.adopted_by.connect(p)
