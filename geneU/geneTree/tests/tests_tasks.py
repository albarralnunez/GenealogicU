from django.test import TestCase
from set_up import setup
from geneTree.tasks import *
from geneTree.gedcom_uploader import GedcomUploader
import os
from django.core.files.uploadedfile import UploadedFile


class tasksTestCase(TestCase):

    def setUp(self):
        self.setup = setup()
        self.setup.clean_up()
        self.setup.light_setup()

    def tearDown(self):
        self.setup.clean_up()

    def test_gedcom_uploader_task(self):
        path = os.path.dirname(os.path.realpath(__file__))
        ged = open(path + '/gedcoms/allged.ged', 'rb')
        ged = UploadedFile(ged)
        ged = GedcomUploader(ged)

        a = gedcom_uploader_task(ged, self.setup.tree)
        self.assertTrue(a)
