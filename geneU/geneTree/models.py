from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom, Relationship, One, DateProperty,
    ZeroOrOne, db)
from geoencoding_node_structure.core import AddressComponent
from datetime import date
from uuid import uuid4

#class Country(StructuredNode):
#    code = StringProperty(unique_index=True, required=True)
#    # traverse incoming IS_FROM relation, inflate to Person objects
#    inhabitant = RelationshipFrom('Person', 'IS_FROM')

class Person(StructuredNode):
    id = StringProperty(unique_index=True, default=uuid4)
    name = StringProperty(required=True)
    surname = StringProperty(index=True)
    second_surname = StringProperty(index=True)
    birth = DateProperty(index=True)
    death = DateProperty(index=True)
    genere = StringProperty(choices=(('M',1),('W',2)))

    # traverse outgoing IS_FROM relations, inflate to Country objects
    #country = RelationshipTo(Country, 'IS_FROM')

    married = Relationship('Person', 'MARRIED')
    divorced = Relationship('Person', 'DIVORCED')
    sons = RelationshipTo('Person', 'SON')
    son_of = RelationshipFrom('Person', 'SON')

    birth_in = RelationshipTo(AddressComponent, 'BIRTH_IN', cardinality=ZeroOrOne)
    death_in = RelationshipTo(AddressComponent, 'DEATH_IN', cardinality=ZeroOrOne)
    lived_in = RelationshipTo(AddressComponent, 'LIFE_IN')
    
    #@db.transaction
    def divorce(self, per):
        if (self.married.is_connected(per)):
            self.married.disconnect(per)
        self.divorced.connect(per)

    def marry(self, per):
        if (self.divorced.is_connected(per)):
            self.divorced.disconnect(per)
        self.married.connect(per)
