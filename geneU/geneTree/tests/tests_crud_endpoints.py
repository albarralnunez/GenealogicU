from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from set_up import setup
from datetime import date


class endpointscrudTestCase(APITestCase):

    def setUp(self):
        self.setup = setup()
        self.setup.clean_up()
        # self.setup.light_setup()
        self.setup.light_setup()

    def tearDown(self):
        self.setup.clean_up()

    def test_get_persons(self):
        '''
        get persons
        '''
        url = reverse('person-list')
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_get_tree(self):
        '''
        get trees
        '''
        url = reverse('tree-list')
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_post_tree(self):
        '''
        create tree
        '''
        url = reverse('tree-list')
        data = {
            'name': 'test',
            'description': 'test'
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_person(self):
        '''
        create person
        '''
        url = reverse('person-list')
        data = {
            'name': 'test',
            'genere': 'F',
            'tree': self.setup.tree.id
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_marriage(self):
        '''
        create marriage
        '''
        url = reverse('marriage-list')
        data = {
            'spouse1': self.setup.person3.id,
            'spouse2': self.setup.person1.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_person_marriage(self):
        '''
        create marriage
        '''
        url = reverse(
            'person-detail',
            kwargs={'id': self.setup.person3.id}
        )
        url += 'marriage/'
        data = {
            'spouse1': self.setup.person1.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_marriage(self):
        '''
        get marriage
        '''
        url = reverse('marriage-list')
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_post_divorce(self):
        '''
        create divorce
        '''
        url = reverse('divorce-list')
        data = {
            'spouse1': self.setup.person3.id,
            'spouse2': self.setup.person1.id,
            'location': self.setup.location,
            'loca'
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_person_divorce(self):
        '''
        create divorce
        '''
        url = reverse(
            'person-detail',
            kwargs={'id': self.setup.person3.id}
        )
        url += 'divorce/'
        data = {
            'spouse1': self.setup.person1.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_divorce(self):
        '''
        get divorce
        '''
        url = reverse('divorce-list')
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_post_birth(self):
        '''
        create birth
        '''
        url = reverse('birth-list')
        data = {
            'father1': self.setup.person2.id,
            'father2': self.setup.person1.id,
            'son': self.setup.person3.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_person_birth(self):
        '''
        create birth
        '''
        url = reverse(
            'person-detail',
            kwargs={'id': self.setup.person3.id}
        )
        url += 'birth/'
        data = {
            'father2': self.setup.person1.id,
            'father1': self.setup.person2.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_birth(self):
        '''
        get birth
        '''
        url = reverse('birth-list')
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_post_death(self):
        '''
        create death
        '''
        url = reverse('death-list')
        data = {
            'death': self.setup.person2.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_person_death(self):
        '''
        create death
        '''
        url = reverse(
            'person-detail',
            kwargs={'id': self.setup.person2.id}
        )
        url += 'death/'
        data = {
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_death(self):
        '''
        get death
        '''
        url = reverse('death-list')
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_post_adoption(self):
        '''
        create adoption
        '''
        url = reverse('adoption-list')
        data = {
            'father1': self.setup.person2.id,
            'father2': self.setup.person1.id,
            'son': self.setup.person3.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_person_adoption(self):
        '''
        create adoption
        '''
        url = reverse(
            'person-detail',
            kwargs={'id': self.setup.person3.id}
        )
        url += 'adoption/'
        data = {
            'father2': self.setup.person1.id,
            'father1': self.setup.person2.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_adoption(self):
        '''
        get adoption
        '''
        url = reverse('adoption-list')
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))

    def test_post_lived(self):
        '''
        create lived
        '''
        url = reverse('lived-list')
        data = {
            'person': self.setup.person2.id,
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_person_lived(self):
        '''
        create lived
        '''
        url = reverse(
            'person-detail',
            kwargs={'id': self.setup.person3.id}
        )
        url += 'lived/'
        data = {
            'location': self.setup.location,
            'descritive_location': 'location',
            'date_being': date(2000, 3, 1),
            'date_end': date(2000, 3, 1)
        }
        response = self.client.post(
            url,
            data=data,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lived(self):
        '''
        get lived
        '''
        url = reverse('lived-list')
        response = self.client.get(
            url,
            format='json',
            HTTP_AUTHORIZATION=self.setup.token_bearer
        )
        self.assertTrue(status.is_success(response.status_code))
