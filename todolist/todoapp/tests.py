# Create your tests here.
import json
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from rest_framework import status
# from rest_framework.test import APITestCase

class ViewsTestCase(TestCase):
    def test_init_load(self):
        """Initial Loading Test"""
        payload = {
            "pcode": "Smile",
            "pname": "3001",
        }
        response = self.client.post(reverse('todoapp:projcode'), json.dumps(payload), content_type='application/json')
        print("response--  projcode--", response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        response = self.client.get(reverse('todoapp:projcode'),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        userobj = User.objects.create(username="priya",password="Admin@123",email="priya@gmail.com",first_name="PM",last_name="M")
        payload = {
           "pcode":1,
           "user_id":1,
           "title":"Checking images detail",
           "content":"Not accepting base 64 data",
           "priority":0,
           "end_date":"2021-03-27"
        }
        response = self.client.post(reverse('todoapp:task'), json.dumps(payload), content_type='application/json')
        print("response--  task--", response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse('todoapp:task'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

