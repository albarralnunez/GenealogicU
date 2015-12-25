from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo, RelationshipFrom, Relationship,
    ZeroOrOne)
from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate
from uuid import uuid4
# from django.core.exceptions.entry import DoesNotExist
from neomodel import db


class Marriage(StructuredNode):
    location = RelationshipTo(
        AddressComponent, 'LOCATION', cardinality=ZeroOrOne)
    date = RelationshipTo(
        Day, 'DATE', cardinality=ZeroOrOne)
    spouses = Relationship('Person', 'MARRIED')


class Divorce(StructuredNode):
    date = RelationshipTo(
        Day, 'DATE', cardinality=ZeroOrOne)
    spouses = Relationship('Person', 'DIVORCED')


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

    married = Relationship(Marriage, 'MARRIED')
    divorced = Relationship(Divorce, 'DIVORCED')
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

    def get_marriages(self):
        res = []
        for marriage in self.married.all():
            for spouse in marriage.spouses.all():
                if spouse.id != self.id:
                    m = {}
                    date = list(marriage.date.all())
                    if date:
                        m['date'] = date[0].id
                    loc = list(marriage.location.all())
                    if loc:
                        m['location'] = loc[0].address
                    m['spouse'] = spouse.id
                    res.append(m)
        return res

    def get_divorces(self):
        res = []
        for marriage in self.divorced.all():
            for spouse in marriage.spouses.all():
                if spouse.id != self.id:
                    m = {}
                    date = list(marriage.date.all())
                    if date:
                        m['date'] = date[0].id
                    m['spouse'] = spouse.id
                    res.append(m)
        return res

    def set_born_in(self, loc):
        for l in self.born_in.all():
            self.born_in.disconnect(l)
        if loc:
            self.born_in.connect(
                Location(address_components=loc).save()
            )

    def set_death_in(self, loc):
        for l in self.death_in.all():
            self.death_in.disconnect(l)
        if loc:
            self.death_in.connect(
                Location(address_components=loc).save()
            )

    def set_lived_in(self, locs):
        for l in self.lived_in.all():
            self.lived_in.disconnect(l)
        for location in locs:
            loc = Location(address_components=location).save()
            self.lived_in.connect(loc)

    def set_sons(self, sons):
        for s in self.sons.all():
            self.sons.disconnect(s)
        for son in sons:
            p = Person.nodes.get(id=son)
            self.sons.connect(p)

    def set_son_of(self, son_of):
        for s in self.son_of.all():
            self.son_of.disconnect(s)
        for father in son_of:
            p = Person.nodes.get(id=father)
            self.son_of.connect(p)

    def set_birth_date_begin(self, birth_date_begin):
        for date in self.birth_date_begin.all():
            self.birth_date_begin.disconnect(date)
        if birth_date_begin:
            bd = NodeDate(birth_date_begin).save()
            self.birth_date_begin.connect(bd)

    def set_birth_date_end(self, birth_date_end):
        for date in self.birth_date_end.all():
            self.birth_date_end.disconnect(date)
        if birth_date_end:
            bd = NodeDate(birth_date_end).save()
            self.birth_date_end.connect(bd)

    def set_death_date_begin(self, death_date_begin):
        for date in self.death_date_begin.all():
            self.death_date_begin.disconnect(date)
        if death_date_begin:
            bd = NodeDate(death_date_begin).save()
            self.death_date_begin.connect(bd)

    def set_death_date_end(self, death_date_end):
        for date in self.death_date_end.all():
            self.death_date_end.disconnect(date)
        if death_date_end:
            bd = NodeDate(death_date_end).save()
            self.death_date_end.connect(bd)

    def set_adopted(self, adopted):
        for d in self.adopted.all():
            self.adopted.disconnect(d)
        for ad in adopted:
            p = Person.nodes.get(id=ad)
            self.adopted.connect(p)

    def set_adopted_by(self, adopted_by):
        for d in self.adopted_by.all():
            self.adopted_by.disconnect(d)
        for ad in adopted_by:
            p = Person.nodes.get(id=ad)
            self.adopted_by.connect(p)

    def set_married(self, married):
        for d in self.married.all():
            self.married.disconnect(d)
        for mar in married:
            spouse = Person.nodes.get(id=mar['spouse'])
            marriage = Marriage().save()
            self.married.connect(marriage)
            spouse.married.connect(marriage)
            if 'location' in mar:
                location = Location(address_components=mar['location']).save()
                marriage.location.connect(location)
            if 'date' in mar:
                date = NodeDate(mar['date']).save()
                marriage.date.connect(date)

    def set_divorced(self, married):
        for d in self.divorced.all():
            self.divorced.disconnect(d)
        for mar in married:
            spouse = Person.nodes.get(id=mar['spouse'])
            marriage = Divorce().save()
            self.divorced.connect(marriage)
            spouse.divorced.connect(marriage)
            if 'date' in mar:
                date = NodeDate(mar['date']).save()
                marriage.date.connect(date)

    def create_relations(self, **data):
        if 'born_in' in data:
            self.set_born_in(data['born_in'])
        if 'death_in' in data:
            self.set_death_in(data['death_in'])
        if 'lived_in' in data:
            self.set_lived_in(data['lived_in'])
        if 'birth_date_begin' in data:
            self.set_birth_date_begin(data['birth_date_begin'])
        if 'death_date_begin' in data:
            self.set_death_date_begin(data['death_date_begin'])
        if 'birth_date_end' in data:
            self.set_birth_date_end(data['birth_date_end'])
        if 'death_date_end' in data:
            self.set_death_date_end(data['death_date_end'])
        if 'son_of' in data:
            self.set_son_of(data['son_of'])
        if 'sons' in data:
            self.set_sons(data['sons'])
        if 'adopted' in data:
            self.set_adopted(data['adopted'])
        if 'adopted_by' in data:
            self.set_adopted_by(data['adopted_by'])
        if 'married' in data:
            self.set_married(data['married'])
        if 'divorced' in data:
            self.set_divorced(data['divorced'])

    def destroy_all_relations(self):
        for rel in self.birth_date_begin.all():
            self.birth_date_begin.disconnect(rel)
        for rel in self.birth_date_end.all():
            self.birth_date_end.disconnect(rel)
        for rel in self.death_date_begin.all():
            self.death_date_begin.disconnect(rel)
        for rel in self.death_date_end.all():
            self.death_date_end.disconnect(rel)
        for rel in self.lived_in.all():
            self.lived_in.disconnect(rel)
        for rel in self.married.all():
            self.married.disconnect(rel)
        for rel in self.divorced.all():
            self.divorced.disconnect(rel)
        for rel in self.sons.all():
            self.sons.disconnect(rel)
        for rel in self.son_of.all():
            self.son_of.disconnect(rel)
        for rel in self.adopted_by.all():
            self.adopted_by.disconnect(rel)
        for rel in self.adopted.all():
            self.adopted.disconnect(rel)
        for rel in self.born_in.all():
            self.born_in.disconnect(rel)
        for rel in self.death_in.all():
            self.death_in.disconnect(rel)

    def set_attr(self, **data):
        if 'name' in data:
            self.name = data.get('name')
        if 'genere' in data:
            self.genere = data.get('genere')
        if 'surname' in data:
            self.surname = data.get('surname')
        if 'second_surname' in data:
            self.second_surname = data.get('second_surname')

    @db.transaction
    def update_person(self, data, rel):
        self.set_attr(**data)
        self.create_relations(**rel)

    @staticmethod
    @db.transaction
    def create_person(data, rel):
        result = Person(**data).save()
        result.create_relations(**rel)
        return result
