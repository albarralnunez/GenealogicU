from neomodel import (
    StructuredNode, StringProperty, One,
    RelationshipTo, RelationshipFrom, Relationship,
    ZeroOrOne, ArrayProperty, BooleanProperty, OneOrMore)
from uuid import uuid4
from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate
# import geneTree.models_person as'


class Tree(StructuredNode):
    id = StringProperty(unique_index=True, default=uuid4)
    name = StringProperty(required=True)
    description = StringProperty()
    private = BooleanProperty(default=False)
    persons = RelationshipTo('Person', 'MEMBER')
    user = Relationship('core.models.UserNode', 'OWN')

    def set_owner(self, owner):
        self.user.connect(owner)

    def get_persons(self):
        return self.persons.all()


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
    married = Relationship('Person', 'MARRIED')

    def add_spouse(self, married):
        self.married.connect(married)

    def get_spouses(self):
        return list(self.married.all())


class Divorce(Event):
    divorced = Relationship('Person', 'DIVORCED')

    def add_spouse(self, married):
        self.divorced.connect(married)

    def get_spouses(self):
        return list(self.divorced.all())


class Birth(Event):
    father = Relationship('Person', 'FATHER')
    son = Relationship('Person', 'SON')

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
    person = Relationship('Person', 'DEATH')

    def set_death(self, death):
        self.person.connect(death)

    def get_person(self):
        a = list(self.person.all())
        if a:
            return a[0]
        else:
            return None


class Adoption(Event):
    father_adpt = Relationship('Person', 'FATHER')
    son_adpt = Relationship('Person', 'SON')

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
    lived_in = Relationship('Person', 'LIVED_IN')

    def set_person(self, person):
        self.lived_in.connect(person)

    def get_person(self):
        a = list(self.lived_in.all())
        if a:
            return a[0]
        else:
            None


class Person(StructuredNode):

    id = StringProperty(unique_index=True, default=uuid4)
    name = StringProperty()
    surname = StringProperty(index=True)
    second_surname = StringProperty(index=True)
    genere = StringProperty(choices=(('M', 1), ('F', 2)))

    married = Relationship('Marriage', 'MARRIED')
    divorced = Relationship('Divorce', 'DIVORCED')
    death = Relationship('Death', 'DEATH')
    father = Relationship('Birth', 'FATHER')
    father_adpt = Relationship('Adoption', 'FATHER')
    son = Relationship('Birth', 'SON')
    son_adpt = Relationship('Adoption', 'SON')
    lived_in = Relationship('Lived', 'LIVED_IN')

    tree = Relationship(Tree, 'MEMBER', cardinality=OneOrMore)

    def set_lieved(
            self, date_begin=None,
            date_end=None, loc=None,
            loc_p=None, description=None
    ):
        b = Lived().save()
        b.set_event(
            loc=loc, location_prop=loc_p, date_begin=date_begin,
            date_end=date_end)
        b.lived_in.connect(self)
        if description:
            self.description = description
        return b

    def set_marriage(
            self, spouse, date_begin=None,
            date_end=None, loc=None, loc_p=None):
        b = Marriage().save()
        b.set_event(
            loc=loc, location_prop=loc_p, date_begin=date_begin,
            date_end=date_end)
        b.married.connect(self)
        if spouse:
            b.married.connect(spouse)
        return b

    def set_divorced(
            self, spouse, date_begin=None, date_end=None,
            loc=None, loc_p=None):
        b = Divorce().save()
        b.set_event(
            loc=loc, location_prop=loc_p,
            date_begin=date_begin, date_end=date_end)
        b.divorced.connect(self)
        if spouse:
            b.divorced.connect(spouse)
        return b

    def set_birth(
            self, date_begin=None, date_end=None,
            loc=None, loc_p=None, father1=None, father2=None):
        if self.son.all():
            raise AttributeError('...')
        b = Birth().save()
        b.set_event(
            loc=loc, location_prop=loc_p,
            date_begin=date_begin, date_end=date_end)
        b.son.connect(self)
        if father1:
            father1.father.connect(b)
        if father2:
            father2.father.connect(b)
        return b

    def set_death(
            self, description=None, date_begin=None, date_end=None,
            loc=None, loc_p=None):
        if self.death.all():
            raise AttributeError('...')
        b = Death().save()
        b.set_event(
            loc=loc, location_prop=loc_p, date_begin=date_begin,
            date_end=date_end)
        b.person.connect(self)
        if description:
            b.description = description
        return b

    def set_adopted(
            self, father1, father2, date_begin=None, date_end=None, loc=None,
            loc_p=None):
        if self.son_adpt.all():
            raise AttributeError('...')
        b = Adoption().save()
        b.set_event(
            loc=loc, location_prop=loc_p, date_begin=date_begin,
            date_end=date_end)
        b.son_adpt.connect(self)
        if father1:
            father2.father_adpt.connect(b)
        if father2:
            father2.father_adpt.connect(b)
        return b

    def set_tree(self, tree):
        self.tree.connect(tree)

    def get_marriages(self):
        return self.married.all()

    def get_divorces(self):
        return self.divorced.all()

    def get_adopted(self):
        a = list(self.son_adpt.all())
        if a:
            return a[0]
        else:
            return None

    def get_birth(self):
        a = list(self.son.all())
        if a:
            return a[0]
        else:
            return None

    def get_death(self):
        a = list(self.death.all())
        if a:
            return a[0]
        else:
            return None

    def get_adoptions(self):
        return self.father_adpt.all()

    def get_father(self):
        return self.father.all()

    def get_lived(self):
        return self.lived_in.all()

    def get_similar_lived(self):
        query = \
            """
            START a=node({self})
            MATCH a-[:FRIEND]->(b)
            RETURN b
            """
        results, columns = self.cypher(query)
        return [self.inflate(row[0]) for row in results]

'''
def get_marriages(self):
    res = []
    for marriage in self.married.all():
        for spouse in marriage.married.all():
            if spouse.id != self.id:
                m = {}
                date = list(marriage.date_begin.all())
                if date:
                    m['date_begin'] = NodeDate.to_date(date[0])
                date = list(marriage.date_end.all())
                if date:
                    m['date_end'] = NodeDate.to_date(date[0])

                loc = list(marriage.location.all())
                if loc:
                    m['location'] = loc[0]
                if marriage.location_prop:
                    m['location_prop'] = marriage.location_prop

                m['spouse'] = spouse
                res.append(m)
    return res

def get_divorces(self):
    res = []
    for marriage in self.divorced.all():
        for spouse in marriage.divorced.all():
            if spouse.id != self.id:
                m = {}
                date = list(marriage.date_begin.all())
                if date:
                    m['date_begin'] = NodeDate.to_date(date[0])
                date = list(marriage.date_end.all())
                if date:
                    m['date_end'] = NodeDate.to_date(date[0])
                m['spouse'] = spouse
                res.append(m)
    return res
'''
