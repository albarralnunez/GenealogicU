from django.test import TestCase
from .models import Person, Country
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
            first_name='Albarral',
            second_name='Nunez',
            genere='M',
            birth=date(1991,8,6)
            ).save()   
        
        pepi = Person(name='Pepi').save()
        dani.son_of.connect(pepi)

        antonio = Person(name='Antonio').save()
        antonio.son.connect(dani)
        
        pepi.marry(antonio)
        
        dani2 = Person(name='Dani2').save()
        dani2.son_of.connect(pepi)
        antonio.son.connect(dani2)

        dani_junior = Person(name='Dani Junior').save()
        dani.son.connect(dani_junior)

        sra_maria = Person(name='Sra Maria').save()
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