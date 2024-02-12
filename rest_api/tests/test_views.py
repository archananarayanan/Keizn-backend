import datetime
import json
from django.test import TestCase

from django.utils import timezone

from rest_api.models import Category, Tags, Stock, Quantity, TagMap
from accounts.models import User

class RestAPIViewTest(TestCase):
    def setUp(self):
        # Create users
        User.objects.create(username='test', password='test', email='test@t.com')
        self.user_login = {
            'username': 'test',
            'password': 'test'
        }
        # Create a stock
        Category.objects.create(name='test')
        cat = Category.objects.get(name="test")
        Stock.objects.create(sku='test', name="test", price=8, category=cat)
        st = Stock.objects.get(sku="test")
        Quantity.objects.create(sku=st, allocated=0, alloc_build=23, alloc_sales=2, available=1, incoming=1, build_order=2, net_stock=1, can_build=1, instock=786)
        Tags.objects.create(name="tag1")
        tag = Tags.objects.get(name="tag1")
        TagMap.objects.create(sku=st, tag=tag)

    def test_logged_in_uses_get_Category(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_login),
            content_type='application/json'
        )
        token = response.data['data']['token']
        headers = {'Authorization': 'Bearer '+token}
        response = self.client.get('/api/get_categories/', headers=headers)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 201)

    def test_logged_in_uses_post_Category(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_login),
            content_type='application/json'
        )
        token = response.data['data']['token']
        headers = {'Authorization': 'Bearer '+token}
        payload = {'name': 'test1'}
        response = self.client.post('/api/create_category/', 
                                    data=json.dumps(payload),
                                    content_type='application/json',
                                    headers=headers)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 201)

    def test_Invalid_in_uses_get_Category(self):
        response = self.client.get('/api/get_categories/')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 403)

    def test_logged_in_uses_get_Tags(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_login),
            content_type='application/json'
        )
        token = response.data['data']['token']
        headers = {'Authorization': 'Bearer '+token}
        response = self.client.get('/api/get_tags/', headers=headers)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 201)

    def test_logged_in_uses_post_Tags(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_login),
            content_type='application/json'
        )
        token = response.data['data']['token']
        headers = {'Authorization': 'Bearer '+token}
        payload = {'name': 'test1'}
        response = self.client.post('/api/create_tags/', 
                                    data=json.dumps(payload),
                                    content_type='application/json',
                                    headers=headers)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 201)

    def test_Invalid_in_uses_get_Tags(self):
        response = self.client.get('/api/get_tags/')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 403)
    
    def test_logged_in_uses_get_Stock(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_login),
            content_type='application/json'
        )
        token = response.data['data']['token']
        headers = {'Authorization': 'Bearer '+token}
        response = self.client.get('/api/get_stock_dashboard/', headers=headers)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 201)

    def test_logged_in_uses_post_Stock(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_login),
            content_type='application/json'
        )
        token = response.data['data']['token']
        headers = {'Authorization': 'Bearer '+token}
        payload = {
        "sku": "BES_W",
        "name": "BeesWax",
        "price": 156,
        "category": "test",
        "allocated": 67,
        "alloc_build": 82,
        "alloc_sales": 67,
        "available": 78,
        "incoming": 45,
        "build_order": 2,
        "net_stock": 56,
        "instock": 675,
        "tags": [
            "test"
        ]
        }
        response = self.client.post('/api/create_category/', 
                                    data=json.dumps(payload),
                                    content_type='application/json',
                                    headers=headers)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 201)

    def test_Invalid_in_uses_get_Stock(self):
        response = self.client.get('/api/get_stock_dashboard/')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 403)
    
    def test_logged_in_uses_get_Stock_filter(self):
        response = self.client.post('/api/login/',
            data=json.dumps(self.user_login),
            content_type='application/json'
        )
        token = response.data['data']['token']
        headers = {'Authorization': 'Bearer '+token}
        response = self.client.get('/api/get_stock_dashboard/?category=cdfs,fret', headers=headers)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 404)
