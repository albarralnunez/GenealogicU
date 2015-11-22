# Create your tests here.
from django.test import TestCase
from .core import Location
import service
from neomodel import db
import sys
import os

class geoencodingTestCase(TestCase):

    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

    def setUp(self):
        example.configure(
            'https://maps.googleapis.com/maps/api/geocode',
            key=(GOOGLE_API_KEY)
        )

#        db.cypher_query(
#            '''
#            MATCH (n)\
#            OPTIONAL MATCH (n)-[r]-()\
#            WITH n,r LIMIT 100000 DELETE n,r;\
#            '''
#        )
        '''
        address_components = [
            {
               "long_name" : "Shinshoji",
               "short_name" : "Shinshoji",
               "types" : [ "sublocality_level_1", "sublocality", "political" ]
            },
            {
               "long_name" : "Jonan Ward",
               "short_name" : "Jonan Ward",
               "types" : [ "ward", "locality", "political" ]
            },
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
            },
            {
               "long_name" : "814-0121",
               "short_name" : "814-0121",
               "types" : [ "postal_code" ]
            }
        ]

        location = Location(address_components)
        '''
    def test(self):
        self.assertEquals(True, True)