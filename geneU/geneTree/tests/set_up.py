from neomodel import db
from core.models import UserNode
from geoencoding_node_structure.core import Location, RootLocation
from date_node_structure.core import NodeDate, RootDate
from django.contrib.auth.models import User
from oauth2_provider.models import Application, AccessToken
from datetime import timedelta, date
from django.utils import timezone
import geneTree.models_person as models_person
import random
import string

bcn = {'address_components': [
    {
        "long_name": "Barcelona",
        "short_name": "Barcelona",
        "types": ["locality", "political"]
    },
    {
        "long_name": "Barcelona",
        "short_name": "Barcelona",
        "types": ["administrative_area_level_4", "political"]
    },
    {
        "long_name": "El Barcelones",
        "short_name": "El Barcelones",
        "types": ["administrative_area_level_3", "political"]
    },
    {
        "long_name": "Barcelona",
        "short_name": "B",
        "types": ["administrative_area_level_2", "political"]
    },
    {
        "long_name": "Catalonia",
        "short_name": "CT",
        "types": ["administrative_area_level_1", "political"]
    },
    {
        "long_name": "Spain",
        "short_name": "ES",
        "types": ["country", "political"]
    }
]}

cat = {'place_id': 'ChIJ8_UwhdxbpBIRUMijIeD6AAE'}

sp = {'address_components': [
    {
        "long_name": "Spain",
        "short_name": "ES",
        "types": ["country", "political"]
    }
]}


gir = {'address_components': [
    {
        "long_name": "Girona",
        "short_name": "Girona",
        "types": ["locality", "political"]
    },
    {
        "long_name": "Girona",
        "short_name": "Girona",
        "types": ["administrative_area_level_4", "political"]
    },
    {
        "long_name": "El Girones",
        "short_name": "El Girones",
        "types": ["administrative_area_level_3", "political"]
    },
    {
        "long_name": "Province of Girona",
        "short_name": "Province of Girona",
        "types": ["administrative_area_level_2", "political"]
    },
    {
        "long_name": "Catalonia",
        "short_name": "CT",
        "types": ["administrative_area_level_1", "political"]
    },
    {
        "long_name": "Spain",
        "short_name": "ES",
        "types": ["country", "political"]
    }
]}

jp = {'address_components': [
    {
        "long_name": "Fukuoka",
        "short_name": "Fukuoka",
        "types": ["locality", "political"]
    },
    {
        "long_name": "Fukuoka Prefecture",
        "short_name": "Fukuoka Prefecture",
        "types": ["administrative_area_level_1", "political"]
    },
    {
        "long_name": "Japan",
        "short_name": "JP",
        "types": ["country", "political"]
    }
]}


class setup():

    def __init__(self, *args, **kwargs):
        self.user = None
        self.token_bearer = None
        self.app = None
        self.person1 = None
        self.person2 = None
        self.person3 = None
        self.tree = None

    def __create_client_app(self, user):
        def _create_authorization_header(token):
            return "Bearer {0}".format(token)

        self.app = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='https://www.none.com/oauth2/callback',
            name='dummy',
            user=user
        )
        access_token = AccessToken.objects.create(
            user=user,
            scope='read write',
            expires=timezone.now() + timedelta(hours=1),
            token='secret-access-token-key',
            application=self.app
        )
        self.token_bearer = _create_authorization_header(access_token)

    def setup(self):

        def set_event(b, loc=None, loc_p=None, date_begin=None, date_end=None):
            if loc:
                b.location.connect(loc)
            if date_begin:
                b.date_begin.connect(date_begin)
            if date_end:
                b.date_end.connect(date_end)
            if loc_p:
                b.location_prop = loc_p

        user = User(username='dummy', email='dummy@geneu.com')
        user.set_password('dummy')
        user.save()
        self.user = user
        self.__create_client_app(user)

        exs = list(RootLocation.nodes.all())
        if not exs:
            RootLocation().save()

        exs = list(RootDate.nodes.all())
        if not exs:
            RootDate().save()

        tree = models_person.Tree(name='Test').save()
        user = UserNode.nodes.get(id=user.id)
        tree.set_owner(user)

        dani = models_person.Person(
            name='Daniel',
            surname='Albarral',
            second_surname='Nunez',
            genere='M'
        ).save()
        tree.persons.connect(dani)
        b = models_person.Birth().save()
        date_begin = NodeDate(date(2010, 5, 24)).save()
        date_end = NodeDate(date(2010, 5, 24)).save()
        location = Location(**bcn).save()
        set_event(
            b=b, loc=location, date_begin=date_begin, date_end=date_end)
        b.son.connect(dani)

        pepi = models_person.Person(
            name='Pepi', surname='Nunez', genere='F').save()
        b.father.connect(pepi)
        tree.persons.connect(pepi)

        antonio = models_person.Person(
            name='Antonio', surname='Albarral', genere='M').save()
        b.father.connect(antonio)
        tree.persons.connect(antonio)
        m = models_person.Marriage().save()
        date_begin = NodeDate(date(2009, 5, 24)).save()
        date_end = NodeDate(date(2010, 6, 24)).save()
        location = Location(**bcn).save()
        set_event(
            b=m, loc=location, date_begin=date_begin, date_end=date_end)
        m.married.connect(pepi)
        m.married.connect(antonio)

        m = models_person.Birth().save()
        date_begin = NodeDate(date(2000, 5, 24)).save()
        date_end = NodeDate(date(2000, 6, 24)).save()
        location = Location(**gir).save()
        set_event(
            b=m, loc=location, date_begin=date_begin, date_end=date_end)
        m.son.connect(antonio)

        sra_maria = models_person.Person(
            name='Maria',
            surname='Izquierdo',
            genere='F').save()
        m.father.connect(sra_maria)

        sr_juanito = models_person.Person(name='Juan', genere='F').save()
        tree.persons.connect(sr_juanito)
        m = models_person.Divorce().save()
        m.divorced.connect(sr_juanito)
        m.divorced.connect(sra_maria)

        random = models_person.Person(name='Random', genere='M').save()

        event1 = {
            'loc': cat,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': random
        }
        models_person.Death.const(**event1)

        self.person1 = antonio
        self.person2 = random
        self.person3 = sr_juanito
        self.tree = tree
        self.location = bcn

    def light_setup(self):
        user = User(username='dummy', email='dummy@geneu.com')
        user.set_password('dummy')
        user.save()
        self.user = user
        self.__create_client_app(user)
        exs = list(RootLocation.nodes.all())
        if not exs:
            RootLocation().save()
        exs = list(RootDate.nodes.all())
        if not exs:
            RootDate().save()
        t = models_person.Tree(name='Test').save()
        user = UserNode.nodes.get(id=user.id)

        t.set_owner(user)

        self.tree = t
        self.person1 = models_person.Person(genere='M').save()
        self.person1.set_tree(self.tree)
        self.person2 = models_person.Person(genere='M').save()
        self.person2.set_tree(self.tree)
        self.person3 = models_person.Person(genere='M').save()
        self.person3.set_tree(self.tree)
        self.location = bcn

    def std(self):
        user = User(username='dummy', email='dummy@geneu.com')
        user.set_password('dummy')
        user.save()
        self.user = user
        self.__create_client_app(user)
        exs = list(RootLocation.nodes.all())
        if not exs:
            RootLocation().save()
        exs = list(RootDate.nodes.all())
        if not exs:
            RootDate().save()
        t1 = models_person.Tree(name='Test1').save()
        t2 = models_person.Tree(name='Test2').save()
        user = UserNode.nodes.get(id=user.id)
        t1.set_owner(user)
        t2.set_owner(user)
        self.tree = t1
        self.person1 = models_person.Person(genere='M', name='person1').save()
        self.person1.set_tree(t1)
        self.person2 = models_person.Person(genere='M', name='person2').save()
        self.person2.set_tree(t2)

    def event_setup_1(self):
        '''
        def corte e2 interseccion e1
        '''
        self.std()
        event1 = {
            'loc': bcn,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': bcn,
            'date_begin': date(1890, 10, 2),
            'date_end': date(1991, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_2(self):
        '''
        def corte e2 interseccion e1
        '''
        self.std()
        event1 = {
            'loc': bcn,
            'date_begin': date(1800, 11, 1),
            'date_end': date(1801, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': bcn,
            'date_begin': date(1700, 10, 2),
            'date_end': date(1900, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_3(self):
        '''
        def corte e2 interseccion e1
        '''
        self.std()
        event1 = {
            'loc': bcn,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': bcn,
            'date_begin': date(1991, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_4(self):
        '''
        def  e2 no interseccion e1
        '''
        self.std()
        event1 = {
            'loc': bcn,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': bcn,
            'date_begin': date(2001, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_5(self):
        '''
        def  e2 no interseccion e1
        '''
        self.std()
        event1 = {
            'loc': bcn,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': jp,
            'date_begin': date(1990, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_6(self):
        '''
        def  e2 no interseccion e1
        '''
        self.std()
        event1 = {
            'loc': bcn,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': cat,
            'date_begin': date(1990, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_7(self):
        '''
        def  e2 no interseccion e1
        '''
        self.std()
        event1 = {
            'loc': sp,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': cat,
            'date_begin': date(1990, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_8(self):
        '''
        def  e2 no interseccion e1
        '''
        self.std()
        event1 = {
            'loc': bcn,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': gir,
            'date_begin': date(1990, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_9(self):
        '''
        def  e2 no interseccion e1
        '''
        self.std()
        event1 = {
            'loc': cat,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': bcn,
            'date_begin': date(1990, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_10(self):
        '''
        def  e2 no interseccion e1
        '''
        self.std()
        event1 = {
            'loc': cat,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': sp,
            'date_begin': date(1990, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup_11(self):
        '''
        def  e2 no interseccion e1
        '''
        self.std()
        event1 = {
            'loc': cat,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)
        event2 = {
            'loc': sp,
            'date_begin': date(1990, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)
        event2 = {
            'loc': jp,
            'date_begin': date(1990, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event2)

    def event_setup(self):
        id = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(10))
        username = 'dummy' + id
        user = User(username=username, email=username+'@geneu.com')
        user.set_password('dummy')
        user.save()
        self.user = user
        self.__create_client_app(user)
        exs = list(RootLocation.nodes.all())
        if not exs:
            RootLocation().save()
        exs = list(RootDate.nodes.all())
        if not exs:
            RootDate().save()
        t1 = models_person.Tree(name='Test1').save()
        t2 = models_person.Tree(name='Test2').save()
        user = UserNode.nodes.get(id=user.id)
        t1.set_owner(user)
        t2.set_owner(user)
        self.tree = t1
        self.person1 = models_person.Person(
            genere='M', name='person1').save()
        self.person1.set_tree(self.tree)
        self.person2 = models_person.Person(
            genere='M', name='person2').save()
        self.person2.set_tree(self.tree)
        self.person3 = models_person.Person(
            genere='M', name='person3').save()
        self.person3.set_tree(self.tree)
        self.person4 = models_person.Person(
            genere='M', name='person4').save()
        self.person4.set_tree(self.tree)
        self.person5 = models_person.Person(
            genere='M', name='person5').save()
        self.person5.set_tree(t2)
        self.location = bcn

        event1 = {
            'loc': cat,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person1
        }
        models_person.Lived.const(**event1)

        event1 = {
            'loc': cat,
            'date_begin': date(2001, 11, 1),
            'date_end': date(2001, 12, 1),
            'person': self.person1
        }
        models_person.Death.const(**event1)

        event2 = {
            'loc': bcn,
            'date_begin': date(1890, 10, 2),
            'date_end': date(1991, 11, 3),
            'person': self.person3
        }
        models_person.Lived.const(**event2)

        event4 = {
            'loc': bcn,
            'date_begin': date(1992, 10, 2),
            'date_end': date(2001, 11, 3),
            'person': self.person3
        }

        models_person.Lived.const(**event4)

        event3 = {
            'loc': sp,
            'date_begin': date(1992, 1, 2),
            'date_end': date(1993, 1, 3),
            'person': self.person2
        }
        models_person.Lived.const(**event3)

        event5 = {
            'loc': jp,
            'date_begin': date(1991, 1, 2),
            'date_end': date(1993, 1, 3),
            'person': self.person4
        }
        models_person.Lived.const(**event5)

        event5 = {
            'loc': bcn,
            'date_begin': date(1890, 1, 2),
            'date_end': date(1890, 1, 3),
            'person': self.person4
        }
        models_person.Lived.const(**event5)

        event5 = {
            'loc': bcn,
            'date_begin': date(1890, 1, 2),
            'date_end': date(1890, 1, 3),
            'person': self.person5
        }
        models_person.Lived.const(**event5)

        event = {
            'loc': cat,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person5
        }
        models_person.Lived.const(**event)

        event = {
            'loc': cat,
            'date_begin': date(1900, 11, 1),
            'date_end': date(2000, 12, 1),
            'person': self.person5
        }
        models_person.Lived.const(**event)

        event1 = {
            'loc': cat,
            'date_begin': date(2001, 11, 1),
            'date_end': date(2001, 12, 1),
            'person': self.person5
        }
        models_person.Death.const(**event1)

    @staticmethod
    def clean_up():
        db.cypher_query(
            '''
            MATCH (n) \
            OPTIONAL MATCH (n)-[r]-() \
            WITH n,r LIMIT 1000 DELETE n,r; \
            '''
        )

        exs = list(RootLocation.nodes.all())
        if not exs:
            RootLocation().save()

        exs = list(RootDate.nodes.all())
        if not exs:
            RootDate().save()
