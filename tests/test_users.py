from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {'username': 'testuser', 'password': 'pass12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
