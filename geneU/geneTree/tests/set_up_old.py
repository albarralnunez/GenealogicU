from neomodel import db
from core.models import UserNode
from geneTree.models import Tree, Person
from geoencoding_node_structure.core import Location
from datetime import date
from django.contrib.auth.models import User
from date_node_structure.core import RootDate
from geoencoding_node_structure.core import RootLocation
from oauth2_provider.models import Application, AccessToken
from datetime import timedelta
from django.utils import timezone


bcn = [
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
]

gir = [
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
 ]

jp = [
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
]


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
            expires=timezone.now() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.app
        )
        self.token_bearer = _create_authorization_header(access_token)

    def setup(self):
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

        tree = Tree(name='Test').save()
        user = UserNode.nodes.get(id=user.id)
        user.own.connect(tree)

        dani = Person(
            name='Daniel',
            surname='Albarral',
            second_surname='Nunez',
            genere='M'
            ).save()

        dani.create_relations(
          birth_date_begin=date(2010, 5, 24),
          birth_date_end=date(2010, 5, 24),
          born_in=bcn,
          tree=tree.id
          )

        dani.create_relations(
          birth_date_begin=date(2010, 5, 23),
          )
        #  dani.birth_date_begin.connect(NodeDate(date(2010, 5, 24)).save())
        #  dani.birth_date_end.connect(NodeDate(date(2010, 5, 24)).save())
        #  dani.born_in.connect(Location(address_components=bcn).save())

        pepi = Person(name='Pepi', surname='Nunez', genere='F').save()
        dani.son_of.connect(pepi)
        tree.persons.connect(pepi)
        # pepi_birth = NeoDate(date(1991,8,6))
        # pepi.birth_on.connect(pepi_birth.day)

        antonio = Person(name='Antonio', surname='Albarral', genere='M').save()
        antonio.sons.connect(dani)
        tree.persons.connect(antonio)
        antonio.born_in.connect(Location(address_components=gir).save())

        antonio.create_relations(
          married=[{
            'spouse': pepi.id, 'date': date(2010, 12, 2), 'location': bcn}]
          )

        dani2 = Person(name='Daniela', surname='Albarral', genere='F').save()
        dani2.son_of.connect(pepi)
        tree.persons.connect(dani2)
        antonio.sons.connect(dani2)

        dani_junior = Person(
            name='Pepi',
            surname='Albarral',
            genere='F').save()
        tree.persons.connect(dani_junior)
        dani.sons.connect(dani_junior)

        sra_maria = Person(
            name='Maria',
            surname='Izquierdo',
            genere='F').save()
        sra_maria.sons.connect(antonio)
        tree.persons.connect(sra_maria)

        sr_juanito = Person(name='Juan').save()
        tree.persons.connect(sr_juanito)
        sr_juanito.create_relations(
          divorced=[{
            'spouse': sra_maria.id, 'date': date(2010, 12, 2)}]
          )

        self.person1 = antonio
        self.person2 = dani2
        self.person3 = sr_juanito
        self.tree = tree

    @staticmethod
    def clean_up():
        db.cypher_query(
                  '''
                  MATCH (n)\
                  OPTIONAL MATCH (n)-[r]-()\
                  WITH n,r LIMIT 100000 DELETE n,r;\
                  '''
              )

        exs = list(RootLocation.nodes.all())
        if not exs:
            RootLocation().save()

        exs = list(RootDate.nodes.all())
        if not exs:
            RootDate().save()
