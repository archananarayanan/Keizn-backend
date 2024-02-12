import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from accounts.models import User

class AccountsViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create 1 user
        User.objects.create(username='test', password='test', email='test@t.com')
        self.valid_payload = {
            'username': 'test1',
            'email': 'test1@t.com',
            'password': 'test1'
        }
        self.invalid_payload = {
            'username': None,
            'email': 'test1@t.com',
            'password': 'test1'
        }
        self.user_login = {
            'username': 'test',
            'password': 'test'
        }
        self.user_invalidlogin = {
            'username': 'test1',
            'password': 'xyz'
        }

    def test_create_valid_user(self):
        response = self.client.post('/api/register/',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = self.client.post('/api/register/',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_valid_user(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_login),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_user(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_invalidlogin),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)