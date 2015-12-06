# Create your tests here.
from django.test import TestCase
from .core import NodeDate, RootDate
from .serializers import *


class DayTestCase(TestCase):

    def setUp(self):
        """
        RootDate().save()

        NodeDate('1991-08-06').save()
        NodeDate('1991-09-06').save()
        NodeDate('1991-09-11').save()
        NodeDate('1992-09-11').save()
        NodeDate('1992-03-11').save()
        NodeDate('1992-09-00').save()
        """
        print '!!!'
        d = NodeDate(year=1992).save()
        serialized_data = DateSerializer(d)
        print serialized_data
        print serialized_data.data

    def test(self):
        self.assertEquals(True, True)
