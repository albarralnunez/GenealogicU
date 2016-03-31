from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from set_up import setup
import os
from django.core.files.uploadedfile import UploadedFile


class endpointsTestCase(APITestCase):

    def setUp(self):
        self.setup = setup()
        self.setup.clean_up()
        self.setup.setup()

    def tearDown(self):
        self.setup.clean_up()
    """
    def test_get_tree_members(self):
        '''
        create tree
        '''
        url = reverse(
            'tree-detail',
            kwargs={'id': self.setup.tree.id}
        )
        url += 'members/'

        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_get_tree_upload(self):
        '''
        create tree
        '''
        path = os.path.dirname(os.path.realpath(__file__))
        url = reverse('tree-list')
        url += 'gedcom/'
        ged = open(path + '/gedcoms/allged.ged', 'rb')
        ged = UploadedFile(ged)
        data = {
                'name': 'tree',
                'file': ged  # UploadedFile(ged)
            }
        response = self.client.post(
            url,
            data=data,
            # files=files,
            format='multipart',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))
    """
    def test_get_person_serach(self):
        '''
        search person
        '''
        url = reverse(
            'person-detail',
            kwargs={'id': self.setup.person1.id}
        )
        url += 'search/'
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        print response
        self.assertTrue(status.is_success(response.status_code))
