from django.urls import reverse
from todo.models import Todo
from rest_framework.test import APITestCase

from todo.serializers import TodoCreateSerializer, TodoDetailSerializer


# Create your tests here.
class TestTodo(APITestCase):
    def setUp(self):
        todo_list = [
            ["TodoA", "TodoA description", True],
            ["TodoB", "TodoB description", False],
            ["TodoC", "TodoC description", False],
        ]

        for todo in todo_list:
            dummy = Todo(title=todo[0], descripttion=todo[1], complete=todo[2])
            dummy.save()

    def test_get_todo_list_without_param(self):
        url = "/todo/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_get_todo_list_with_complete_true(self):
        url = "/todo/?complete=true"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_todo_list_with_complete_false(self):
        url = "/todo/?complete=false"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_todo_list_with_complete_400(self):
        url = "/todo/?complete=fjskfjwei3"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

    def test_get_todo_detail(self):
        todo = Todo.objects.get(title="TodoA")

        url = f"/todo/{todo.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "TodoA")

    def test_get_todo_detail_not_found(self):
        url = "/todo/1000/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_create_todo(self):
        url = "/todo/"
        dummy = {
            "title": "test dummy",
            "descripttion": "더미 테스트 디스크립션",
            "important": "False",
        }

        response = self.client.post(url, data=dummy)

        cmp = Todo.objects.get(title="test dummy")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(dummy["title"], cmp.title)

    def test_update_todo(self):
        # given
        todoA = Todo.objects.get(title="TodoA")
        url = f"/todo/{todoA.id}/"

        data = {
            "title": "todoTest",
            "descripttion": "put method test",
            "important": False,
        }
        # when
        response = self.client.put(url, data=data)
        # then
        response = self.client.get(url)

        self.assertEqual(response.json()["title"], "todoTest")

    def test_update_todo_400(self):
        # given
        todoA = Todo.objects.get(title="TodoA")
        url = f"/todo/{todoA.id}/"

        data = {"descripttion": "400"}
        # when
        response = self.client.put(url, data=data)

        # then
        self.assertEqual(response.status_code, 400)

    def test_update_todo_404(self):
        # given
        url = f"/todo/{392393929}/"
        dummy = {
            "title": "test dummy",
            "descripttion": "더미 테스트 디스크립션",
            "important": "False",
        }
        # when
        response = self.client.put(url, data=dummy)

        # then
        self.assertEqual(response.status_code, 404)

    def test_delete_todo(self):
        # given
        todoA = Todo.objects.get(title="TodoA")
        url = f"/todo/{todoA.id}/"
        # when
        response = self.client.delete(url)

        # then
        result = self.client.get(url)

        self.assertEqual(result.status_code, 404)

    def test_delete_todo_not_found(self):
        # given
        url = f"/todo/{13812938129}/"
        # when
        response = self.client.delete(url)
        # then
        self.assertEqual(response.status_code, 404)
