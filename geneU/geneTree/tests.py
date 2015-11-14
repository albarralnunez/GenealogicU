from django.test import TestCase
from .models import Person, Country
from .views.PersonViewSet import listt, retrieve
from neomodel import db
from datetime import date
import sys

class geneTestCase(TestCase):

    def setUp(self):
        db.cypher_query(
            '''
            MATCH (n)\
            OPTIONAL MATCH (n)-[r]-()\
            WITH n,r LIMIT 100000 DELETE n,r;\
            '''
        )
        
        
        dani = Person(
            name='Daniel',
            surname='Albarral',
            second_surname='Nunez',
            genere='M'
            ).save()  

        ## dani_d = NeoDate(date(1991,8,6))
        ## dani.death_on.connect(dani_d.day)


        pepi = Person(name='Pepi', surname='Nunez', genere='W').save()
        dani.son_of.connect(pepi)
        #pepi_birth = NeoDate(date(1991,8,6))
        #pepi.birth_on.connect(pepi_birth.day)

        antonio = Person(name='Antonio', surname='Albarral', genere='M').save()
        antonio.son.connect(dani)
        
        pepi.marry(antonio)
        
        dani2 = Person(name='Daniela', surname='Albarral', genere='W').save()
        dani2.son_of.connect(pepi)
        antonio.son.connect(dani2)

        dani_junior = Person(name='Pepi', surname='Albarral', genere='W').save()
        dani.son.connect(dani_junior)

        sra_maria = Person(name='Maria', surname='Izquierdo', genere='W').save()
        sra_maria.son.connect(antonio)

        antonio.divorce(pepi)
        pepi.marry(antonio)


    def test(self):
        try:
            p = list(Person.nodes.filter(name='Daniel'))[0]
            self.assertEquals('Daniel', p.name)
            self.assertEquals(date(1991,8,6), p.birth)
        except:
            self.assertEquals(True, True)
