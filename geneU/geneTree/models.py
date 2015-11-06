from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom, Relationship, One, DateProperty,
    db)
from datetime import date
from uuid import uuid4


class Country(StructuredNode):
    code = StringProperty(unique_index=True, required=True)
    # traverse incoming IS_FROM relation, inflate to Person objects
    inhabitant = RelationshipFrom('Person', 'IS_FROM')


class Person(StructuredNode):

    id = StringProperty(unique_index=True, default=uuid4)
    name = StringProperty(index=True)
    first_name = StringProperty(index=True)
    second_name = StringProperty(index=True)
    birth = DateProperty(index=True)
    genere = StringProperty()
    death = DateProperty(index=True)

    # traverse outgoing IS_FROM relations, inflate to Country objects
    country = RelationshipTo(Country, 'IS_FROM')

    married = Relationship('Person', 'MARRIED')
    divorced = Relationship('Person', 'DIVORCED')
    son = RelationshipTo('Person', 'SON')
    son_of = RelationshipFrom('Person', 'SON')

    #@db.transaction
    def divorce(self, per):
        if (self.married.is_connected(per)):
            self.married.disconnect(per)
        self.divorced.connect(per)

    def marry(self, per):
        if (self.divorced.is_connected(per)):
            self.divorced.disconnect(per)
        self.married.connect(per)
