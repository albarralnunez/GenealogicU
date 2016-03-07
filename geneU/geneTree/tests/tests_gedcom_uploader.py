from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from set_up import setup
import os
from django.core.files.uploadedfile import UploadedFile
from geneTree.gedcom_uploader import GedcomUploader


class gedcom_uploaderTestCase(APITestCase):

    def setUp(self):
        self.setup = setup()
        self.setup.clean_up()
        self.setup.light_setup()

    def tearDown(self):
        self.setup.clean_up()

    def test_get_tree_members(self):
        '''
        create tree
        '''
        path = os.path.dirname(os.path.realpath(__file__))
        ged = open(path + '/gedcoms/allged.ged', 'rb')
        ged = UploadedFile(ged)
        a = GedcomUploader(ged)
        a.upload(self.setup.tree)
