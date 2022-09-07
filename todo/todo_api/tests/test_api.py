from django.contrib.auth.models import User
from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, CoreAPIClient, APIClient
from rest_framework import status

from django.db import connection
from django.test.utils import CaptureQueriesContext

from ..models import Todo
from ..serializers import TodoSerializer
# todos/api/<int:todo_id>/
from rest_framework.authtoken.models import Token


class TestTodoApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username1', password='qwerty')
        self.todo_1 = Todo.objects.create(task='Test todo 1', completed=False, user=self.user)
        self.todo_2 = Todo.objects.create(task='Test todo 2', completed=False, user=self.user)
        self.todo_3 = Todo.objects.create(task='Test todo 3', completed=False, user=self.user)
        self.user2 = User.objects.create(username='test_username2')

    def test_get_url_unauthenticated_user(self):
        response = self.client.get(reverse('get_all_todo'))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_url_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('get_all_todo'))
        # print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 3)

    def test_add_new_todo(self):
        self.client.force_authenticate(user=self.user)
        data = {'task': 'Test new todo',
                'completed': False,
                'timestamp': '2022-09-07T12:46:22.987036Z',
                'updated': '2022-09-07T12:46:22.987036Z',
                'user': 1,
                #'user': 'test_username1',
                }
        response = self.client.post(reverse('get_all_todo'), data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        print(response.data)
        self.assertEqual(response.data, data)
        # response = self.client.get(reverse('get_all_todo'))
        # self.assertEqual(len(response.data), 4)
