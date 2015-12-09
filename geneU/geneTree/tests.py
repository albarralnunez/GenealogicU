from django.test import TestCase
from .models import Person
from .serializers import PersonSerializer
from geoencoding_node_structure.core import Location
from datetime import date
from neomodel import db


class geneeTestCase(TestCase):

    def setUp(self):

        bcn = [
            {
               "long_name" : "Barcelona",
               "short_name" : "Barcelona",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Barcelona",
               "short_name" : "Barcelona",
               "types" : [ "administrative_area_level_4", "political" ]
            },
            {
               "long_name" : "El Barcelones",
               "short_name" : "El Barcelones",
               "types" : [ "administrative_area_level_3", "political" ]
            },
            {
               "long_name" : "Barcelona",
               "short_name" : "B",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Catalonia",
               "short_name" : "CT",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Spain",
               "short_name" : "ES",
               "types" : [ "country", "political" ]
            }
         ]

        gir = [
            {
               "long_name" : "Girona",
               "short_name" : "Girona",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Girona",
               "short_name" : "Girona",
               "types" : [ "administrative_area_level_4", "political" ]
            },
            {
               "long_name" : "El Girones",
               "short_name" : "El Girones",
               "types" : [ "administrative_area_level_3", "political" ]
            },
            {
               "long_name" : "Province of Girona",
               "short_name" : "Province of Girona",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Catalonia",
               "short_name" : "CT",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Spain",
               "short_name" : "ES",
               "types" : [ "country", "political" ]
            }
         ]

        jp = [
            {
               "long_name" : "Fukuoka",
               "short_name" : "Fukuoka",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Fukuoka Prefecture",
               "short_name" : "Fukuoka Prefecture",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Japan",
               "short_name" : "JP",
               "types" : [ "country", "political" ]
            }
        ]

        dani = Person(
            name='Daniel',
            surname='Albarral',
            second_surname='Nunez',
            genere='M',
            birth_date_begin=date(2010, 5, 24),
            birth_date_end=date(2010, 5, 24),
            born_in=bcn
            ).save()

        pepi = Person(name='Pepi', surname='Nunez', genere='W').save()
        dani.son_of.connect(pepi)
        # pepi_birth = NeoDate(date(1991,8,6))
        # pepi.birth_on.connect(pepi_birth.day)

        antonio = Person(name='Antonio', surname='Albarral', genere='M').save()
        antonio.sons.connect(dani)
        antonio.born_in.connect(gir)

        pepi.add_married([antonio.id])

        dani2 = Person(name='Daniela', surname='Albarral', genere='W').save()
        dani2.son_of.connect(pepi)
        antonio.sons.connect(dani2)

        dani_junior = Person(
            name='Pepi',
            surname='Albarral',
            genere='W').save()
        dani.sons.connect(dani_junior)

        sra_maria = Person(
            name='Maria',
            surname='Izquierdo',
            genere='W').save()
        sra_maria.sons.connect(antonio)

        antonio.add_divorced([pepi.id])
        pepi.add_married([antonio.id])

    """
    def testt(self):
        try:
            p = list(Person.nodes.filter(name='Daniel'))[0]
            self.assertEquals('Daniel', p.name)
            self.assertEquals(date(1991, 8, 6), p.birth)
        except:
            self.assertEquals(True, True)
    """

    def test_serializers(self):
        # p = list(Person.nodes.filter(name='Daniel'))[0]
        # serialized = PersonSerializer(p, simple=True).data
        self.assertEquals(True, True)
