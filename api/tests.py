from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class GetAllItemTestCase(TestCase):

    """ Test for GET-request, which find all records in REDIS storage """

    def setUp(self):
        self.client = APIClient()
        self.key_value = "get_all_test"
        self.url = 'all_items'

    def test_api_get(self):
        # Create test record
        self.client.post(self.url, {self.key_value: 'unittest'}, format='json')

        # Test GET-request
        response = self.client.get(reverse(self.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete test record
        self.client.delete(reverse('single_item', kwargs={'key': self.key_value}), format='json', follow=True)


class PostItemTestCase(TestCase):

    """ Test for POST-request, which create new record in REDIS storage """

    def setUp(self):
        self.client = APIClient()
        self.key_value = self.key = 'post_test'
        self.value = 'unittest'
        self.url = 'http://localhost:8000/api/items'

    def test_api_post(self):
        # Test POST-request
        response = self.client.post(self.url, {self.key: self.value}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Delete test record
        self.client.delete(reverse('single_item', kwargs={'key': self.key_value}), format='json', follow=True)


class GetSingleItemTestCase(TestCase):

    """ Test for GET-request, which find some record in REDIS storage """

    def setUp(self):
        self.client = APIClient()
        self.key_value = 'get_single_test'
        self.url = 'single_item'

    def test_api_get(self):
        # Create test record
        self.client.post('http://localhost:8000/api/items', {self.key_value: 'unittest'}, format='json')

        # Test GET-request
        response = self.client.get(reverse(self.url, kwargs={'key': self.key_value}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete test record
        self.client.delete(reverse('single_item', kwargs={'key': self.key_value}), format='json', follow=True)


class DeleteSingleItemTestCase(TestCase):

    """ Test for DELETE-request, which delete some record in REDIS storage """

    def setUp(self):
        self.client = APIClient()
        self.key_value = 'delete_test'
        self.url = 'single_item'

    def test_api_delete(self):
        # Create test record
        response = self.client.post('http://localhost:8000/api/items', {self.key_value: 'unittest'}, format='json')

        # Test DELETE-request
        response = self.client.delete(reverse(self.url, kwargs={'key': self.key_value}), format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
