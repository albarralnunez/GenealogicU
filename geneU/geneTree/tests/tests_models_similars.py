# -*- coding: utf-8 -*-

from geneTree.models_person import *
from geneTree.models_event import *
from django.test import TestCase
from set_up import setup


class models_similarsTestCase(TestCase):

    def setUp(self):
        self.setup = setup()
        self.setup.clean_up()

    def tearDown(self):
        self.setup.clean_up()

    def test_get_similar_lived_1(self):
        print '----------------------'
        print 'test_similar_lived_1'
        self.setup.event_setup_1()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([self.setup.person2.name])
        )

    def test_get_similar_lived_2(self):
        print '----------------------'
        print 'test_similar_lived_2'
        self.setup.event_setup_2()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([self.setup.person2.name])
        )

    def test_get_similar_lived_3(self):
        print '----------------------'
        print 'test_similar_lived_3'
        self.setup.event_setup_3()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([self.setup.person2.name])
        )

    def test_get_similar_lived_4(self):
        print '----------------------'
        print 'test_similar_lived_4'
        self.setup.event_setup_4()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([])
        )

    def test_get_similar_lived_5(self):
        print '----------------------'
        print 'test_similar_lived_5'
        self.setup.event_setup_5()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([])
        )

    def test_get_similar_lived_6(self):
        print '----------------------'
        print 'test_similar_lived_6'
        self.setup.event_setup_6()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([self.setup.person2.name])
        )

    def test_get_similar_lived_7(self):
        print '----------------------'
        print 'test_similar_lived_7'
        self.setup.event_setup_7()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([])
        )

    def test_get_similar_lived_8(self):
        print '----------------------'
        print 'test_similar_lived_8'
        self.setup.event_setup_8()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([])
        )

    def test_get_similar_lived_9(self):
        print '----------------------'
        print 'test_similar_lived_9'
        self.setup.event_setup_9()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([])
        )

    def test_get_similar_lived_10(self):
        print '----------------------'
        print 'test_similar_lived_10'
        self.setup.event_setup_10()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([self.setup.person2.name])
        )

    def test_get_similar_lived_11(self):
        print '----------------------'
        print 'test_similar_lived_11'
        self.setup.event_setup_11()
        b = self.setup.person1.get_similar_lived()
        res = map(lambda x: Person.get(x), b)
        self.assertEqual(
            set([x.name for x in res]),
            set([self.setup.person2.name])
        )
