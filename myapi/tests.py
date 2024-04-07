from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserViewSetTestCase(APITestCase):
    def test_create_user(self):
        url = reverse('user-list') 
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User',
            'referral_code': 'ABC123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserDetailsAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_user_details(self):
        user = User.objects.create_user(email='test@example.com', password='password123', name='Test User')
        url = reverse('user-detail', args=[user.id])
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 

class ReferralsAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_referrals(self):
        user = User.objects.create_user(email='test@example.com', password='password123', name='Test User', referral_code='123456')
        url = reverse('referrals')
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# >>
# Found 3 test(s).
# Creating test database for alias 'default'...
# System check identified no issues (0 silenced).
# C:\Users\LENOVO\AppData\Local\Programs\Python\Python311\Lib\site-packages\rest_framework\pagination.py:200: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered 
# object_list: <class 'myapi.models.User'> QuerySet.
#   paginator = self.django_paginator_class(queryset, page_size)
# ...
# ----------------------------------------------------------------------
# Ran 3 tests in 2.188s

# OK
# Destroying test database for alias 'default'...