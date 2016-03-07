from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate
# import geneTree.models_person as models_personn
from neomodel import (
    StructuredNode, StringProperty, One,
    RelationshipTo, RelationshipFrom, Relationship,
    ZeroOrOne, ArrayProperty, BooleanProperty, OneOrMore)
from uuid import uuid4


class Event(StructuredNode):
    id = StringProperty(unique_index=True, default=uuid4)
    location = RelationshipTo(
        AddressComponent, 'LOCATION', cardinality=ZeroOrOne)
    location_prop = StringProperty()
    date_begin = RelationshipTo(
        Day, 'DATE_BEGIN', cardinality=ZeroOrOne)
    date_end = RelationshipTo(
        Day, 'DATE_END', cardinality=ZeroOrOne)
    description = StringProperty()

    def set_event(
            self, loc=None, location_prop=None, description=None,
            date_begin=None, date_end=None):
        if loc:
            loc = Location(address_components=loc).save()
            self.location.connect(loc)
        if date_begin:
            date_begin = NodeDate(date_begin).save()
            self.date_begin.connect(date_begin)
        if date_end:
            date_end = NodeDate(date_end).save()
            self.date_end.connect(date_end)
        if location_prop:
            self.location_prop = location_prop
        if description:
            self.description = description


class Marriage(Event):
    married = Relationship('models_personn.Person', 'MARRIED')

    def add_spouse(self, married):
        self.married.connect(married)

    def get_spouses(self):
        return list(self.married.all())


class Divorce(Event):
    divorced = Relationship('models_personn.Person', 'DIVORCED')

    def add_spouse(self, married):
        self.divorced.connect(married)

    def get_spouses(self):
        return list(self.divorced.all())


class Birth(Event):
    father = Relationship('models_personn.Person', 'FATHER')
    son = Relationship('models_personn.Person', 'SON')

    def add_father(self, father):
        self.father.connect(father)

    def set_son(self, son):
        self.son.connect(son)

    def get_fathers(self):
        return list(self.father.all())

    def get_son(self):
        a = list(self.son.all())
        if a:
            return a[0]
        else:
            return None


class Death(Event):
    person = Relationship('models_personn.Person', 'DEATH')

    def set_death(self, death):
        self.person.connect(death)

    def get_person(self):
        a = list(self.person.all())
        if a:
            return a[0]
        else:
            return None


class Adoption(Event):
    father_adpt = Relationship('models_personn.Person', 'FATHER')
    son_adpt = Relationship('models_personn.Person', 'SON')

    def add_father(self, father):
        self.father_adpt.connect(father)

    def set_son(self, son):
        self.son_adpt.connect(son)

    def get_son(self):
        a = list(self.son_adpt.all())
        if a:
            return a[0]
        else:
            None

    def get_fathers(self):
        return list(self.father_adpt.all())


class Lived(Event):
    lived_in = Relationship('models_personn.Person', 'LIVED_IN')

    def set_person(self, person):
        self.lived_in.connect(person)

    def get_person(self):
        a = list(self.lived_in.all())
        if a:
            return a[0]
        else:
            None
