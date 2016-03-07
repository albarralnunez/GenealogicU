# Create your tests here.
from .core import NodeDate, RootDate
from .serializers import *
from django.test import TestCase


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

    def test(self):
        self.assertEquals(True, True)
