# from .core import Location
from django.test import TestCase


class geoencodingTestCase(TestCase):

    def setUp(self):
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
            }
        ]

        address_components = [
            {
               "long_name" : "Carrer de la Torre Dulac",
               "short_name" : "Carrer de la Torre Dulac",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Barcelona",
               "short_name" : "Barcelona",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Barcelona",
               "short_name" : "B",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "Catalunya",
               "short_name" : "CT",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Spain",
               "short_name" : "ES",
               "types" : [ "country", "political" ]
            }
         ]

        loc = Location(address_components=address_components).save()

        loc = list(Location().get(address_components))

        print loc[0].components if loc else 'not found the location'
        '''

    def test(self):
        self.assertEquals(True, True)
