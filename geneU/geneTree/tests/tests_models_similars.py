# -*- coding: utf-8 -*-

from datetime import date
from geneTree.models_person import *
from geneTree.models_event import *
from django.test import TestCase
from set_up import setup
from geoencoding_node_structure.core import AddressComponent, Location
from date_node_structure.core import Day, NodeDate


class models_similarsTestCase(TestCase):

    def setUp(self):
        self.setup = setup()
        self.setup.clean_up()
        self.setup.event_setup()
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

    def test_get_similar_lived(self):
        b = self.setup.person1.get_similar_lived()
        print [x.name for x in b]
        self.assertEqual([x.name for x in b], [self.setup.person3.name])
