from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class ApiTestCase(TestCase):

    """ Contain tests for all API methods """

    def setUp(self):

        """ Set main params for testing"""

        # Universal
        self.client = APIClient()
        self.value = 'unittest'

        # For all items
        self.all_url = 'all_items'
        self.get_all_key = "get_all_test"
        self.post_key = 'post_test'
        self.post_url ='http://localhost:8000/api/items'

        # For single items
        self.single_url = 'single_item'
        self.get_single_key = 'get_all_test'
        self.put_key = 'put_test'
        self.put_value = 'upd_unittest'
        self.delete_key = 'delete_test'

    def test_api_get_all_items(self):

        """ Test for GET-request, which find all records in REDIS storage """

        # Create test record
        self.client.post(self.post_url, {self.get_all_key: self.value}, format='json')

        # Test GET-request
        response = self.client.get(reverse(self.all_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete test record
        self.client.delete(reverse('single_item', kwargs={'key': self.get_all_key}), format='json', follow=True)

    def test_api_post(self):

        """ Test for POST-request, which create new record in REDIS storage """

        # Test POST-request
        response = self.client.post(self.post_url, {self.post_key: self.value}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Delete test record
        self.client.delete(reverse('single_item', kwargs={'key': self.value}), format='json', follow=True)

    def test_api_get_single_item(self):

        """ Test for GET-request, which find single record in REDIS storage """

        # Create test record
        self.client.post(self.post_url, {self.get_single_key: self.value}, format='json')

        # Test GET-request
        response = self.client.get(reverse(self.single_url, kwargs={'key': self.get_single_key}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete test record
        self.client.delete(reverse('single_item', kwargs={'key': self.get_single_key}), format='json', follow=True)

    def test_api_put(self):

        """ Test for GET-request, which update single record in REDIS storage """

        # Create test record
        self.client.post(self.post_url, {self.put_key: self.value}, format='json')

        # Test PUT-request
        response = self.client.put(reverse(self.single_url, kwargs={'key': self.put_key}), {'new_value': self.put_value}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete test record
        self.client.delete(reverse('single_item', kwargs={'key': self.put_key}), format='json', follow=True)

    def test_api_delete(self):

        """ Test for GET-request, which find delete single record in REDIS storage """

        # Create test record
        self.client.post(self.post_url, {self.delete_key: 'unittest'}, format='json')

        # Test DELETE-request
        response = self.client.delete(reverse(self.single_url, kwargs={'key': self.delete_key}), format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
