from django.test import TestCase
from set_up import setup
from geneTree.tasks import *
from geneTree.gedcom_uploader import GedcomUploader
import os
from django.core.files.uploadedfile import UploadedFile
import time
import sys


class tasksTestCase(TestCase):

    def setUp(self):
        self.setup = setup()
        self.setup.clean_up()

    def tearDown(self):
        self.setup.clean_up()

    def test_gedcom_uploader_task(self):
        self.setup.light_setup()
        path = os.path.dirname(os.path.realpath(__file__))
        ged = open(path + '/gedcoms/allged.ged', 'rb')
        ged = UploadedFile(ged)
        ged = GedcomUploader(ged)

        a = gedcom_uploader_task(ged, self.setup.tree)
        self.assertTrue(a)

    def test_check_coincidence(self):
        print 'test_check_coincidence'
        # setup toolbar
        stp = 2
        sys.stdout.write("[%s]" % (" " * stp))
        sys.stdout.flush()
        sys.stdout.write("\b" * (stp+1))

        sys.stdout.write("\n")
        for x in xrange(stp):
            sys.stdout.write("-")
            sys.stdout.flush()
            self.setup.event_setup()

        sys.stdout.write("\n")
        start_time = time.time()
        check_coincidence_task(self.setup.person1.id)
        print("--- %s seconds ---" % (time.time() - start_time))
        self.assertTrue(True)

    def test_check_coincidence_async(self):
        print 'test_check_coincidence'
        # setup toolbar
        self.setup.event_setup()
        check_coincidence_task.apply_async((self.setup.person1.id,))
        self.assertTrue(True)
