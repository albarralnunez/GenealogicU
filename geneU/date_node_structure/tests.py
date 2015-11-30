# Create your tests here.
from django.test import TestCase
from .core import NodeDate, RootDate
from geocode_service import *
from neomodel import db
import sys
import os

class DayTestCase(TestCase):

    def setUp(self):


        db.cypher_query(
            '''
            MATCH (n)\
            OPTIONAL MATCH (n)-[r]-()\
            WITH n,r LIMIT 100000 DELETE n,r;\
            '''
        )
        
        RootDate().save()

        NodeDate('1991-08-06').save()
        NodeDate('1991-09-06').save()
        NodeDate('1991-09-11').save()
        NodeDate('1992-09-11').save()
        NodeDate('1992-03-11').save()
        NodeDate('1992-09-00').save()


    def test(self):
        self.assertEquals(True, True)