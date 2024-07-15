from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Employee, Store, Visit


class APITestCase(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.client = APIClient()
        self.employee1 = Employee.objects.get(pk=1)
        self.employee2 = Employee.objects.get(pk=3)
        self.employee3 = Employee.objects.get(pk=4)
        self.store1 = Store.objects.get(pk=1)
        self.store2 = Store.objects.get(pk=2)
        self.store3 = Store.objects.get(pk=3)

    def test_get_store_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Phone 89998887766')
        response = self.client.get(reverse('store-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "TSUM")
        self.assertEqual(response.data[1]['name'], "GUM")

    def test_get_store_list_no_stores(self):
        self.client.credentials(HTTP_AUTHORIZATION='Phone 89997770505')
        response = self.client.get(reverse('store-list'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No stores found for this employee.')

    def test_get_store_list_invalid_phone(self):
        self.client.credentials(HTTP_AUTHORIZATION='Phone 1111111111')
        response = self.client.get(reverse('store-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Invalid phone number.')

    def test_post_create_visit(self):
        self.client.credentials(HTTP_AUTHORIZATION='Phone 89998887766')
        data = {
            'store_id': self.store1.pk,
            'latitude': 50.01,
            'longitude': 40.01
        }
        response = self.client.post(reverse('visit-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('date_time', response.data)

    def test_post_create_visit_invalid_store(self):
        self.client.credentials(HTTP_AUTHORIZATION='Phone 89998887766')
        data = {
            'store_id': self.store3.pk,  # Store 3 belongs to a different employee
            'latitude': 50.01,
            'longitude': 40.01
        }
        response = self.client.post(reverse('visit-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_create_visit_invalid_phone(self):
        self.client.credentials(HTTP_AUTHORIZATION='Phone 1111111111')
        data = {
            'store_id': self.store1.pk,
            'latitude': 50.01,
            'longitude': 40.01
        }
        response = self.client.post(reverse('visit-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
