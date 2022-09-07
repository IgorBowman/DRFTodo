from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Todo


class TestTodoApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username1', password='qwerty')
        self.todo_1 = Todo.objects.create(task='Test todo 1', completed=False, user=self.user)
        self.todo_2 = Todo.objects.create(task='Test todo 2', completed=False, user=self.user)
        self.todo_3 = Todo.objects.create(task='Test todo 3', completed=False, user=self.user)
        self.user2 = User.objects.create(username='test_username2')

    def test_get_url_unauthenticated_user(self):
        response = self.client.get(reverse('get_all_todo'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_url_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('get_all_todo'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 3)

    def test_add_new_todo(self):
        self.client.force_authenticate(user=self.user)
        data = {'task': 'Test new todo',
                'completed': False,
                'user': 1,
                }
        response = self.client.post(reverse('get_all_todo'), data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['task'], data['task'])
        self.assertEqual(4, Todo.objects.all().count())

    def test_get_one_todo(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('get_single_todo', kwargs={'todo_id': self.todo_1.pk}))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_todo(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('get_single_todo', kwargs={'todo_id': self.todo_1.pk}))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, Todo.objects.all().count())

