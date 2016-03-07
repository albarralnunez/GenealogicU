# -*- coding: utf-8 -*-

from datetime import date
from geneTree.models_person import *
from geneTree.models_event import *
from django.test import TestCase
from set_up import setup
from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate


class modelsTestCase(TestCase):

    def setUp(self):
        self.setup = setup()
        self.setup.clean_up()
        self.setup.setup()
        self.jp = [
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

    def tearDown(self):
        self.setup.clean_up()

    def test_set_lived(self):
        b = self.setup.person1.set_lieved(
            date_begin=date(2011, 5, 24),
            date_end=date(2011, 5, 25),
            loc=self.jp,
            loc_p='test'
        )
        self.assertTrue(b)

    def test_set_marriage(self):
        b = self.setup.person1.set_marriage(
            date_begin=date(2011, 5, 24),
            date_end=date(2011, 5, 25),
            loc=self.jp,
            loc_p='test',
            spouse=self.setup.person2
        )
        self.assertTrue(b)

    def test_set_divorced(self):
        b = self.setup.person1.set_marriage(
            date_begin=date(2011, 5, 24),
            date_end=date(2011, 5, 25),
            loc=self.jp,
            loc_p='test',
            spouse=self.setup.person2
        )
        self.assertTrue(b)

    def test_set_birth(self):
        b = self.setup.person2.set_birth(
            date_begin=date(2011, 5, 24),
            date_end=date(2011, 5, 25),
            loc=self.jp,
            loc_p='test',
            father1=self.setup.person2,
            father2=self.setup.person3
        )
        self.assertTrue(b)

    def test_set_death(self):
        b = self.setup.person1.set_death(
            date_begin=date(2011, 5, 24),
            date_end=date(2011, 5, 25),
            loc=self.jp,
            loc_p='test'
        )
        self.assertTrue(b)

    def test_set_adopted(self):
        b = self.setup.person1.set_adopted(
            date_begin=date(2011, 5, 24),
            date_end=date(2011, 5, 25),
            loc=self.jp,
            loc_p='test',
            father1=self.setup.person2,
            father2=self.setup.person3
        )
        self.assertTrue(b)

    def test_get_similar_lived(self):
        b = self.setup.person1.get_similar_lived()
        print b
        self.assertEqual(True, True)

    """
    def test_get_marriages(self):
        p = self.setup.person1
        marriages = p.get_marriages()
        expected = [{
                    'spouse': Person.nodes.get(name='Pepi', surname='Nunez'),
                    'date_begin': date(2009, 5, 24),
                    'date_end': date(2010, 6, 24),
                    'location': AddressComponent.nodes.get(
                        formatted_address=
        u'Barcelona, Barcelona, El Barcelonès, Barcelona, Catalonia, Spain')
                    }]
        self.assertEqual(marriages, expected)

    def test_get_divorces(self):
        p = self.setup.person3
        marriages = p.get_divorces()
        expected = [{'spouse': Person.nodes.get(name='Maria')}]
        self.assertEqual(marriages, expected)
    """
