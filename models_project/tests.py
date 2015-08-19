from django.utils import unittest
from models_project.models import Group, Student
from django.test.client import Client


class SimpleTest(unittest.TestCase):

    def setUp(self):
        self.c = Client()

    def test_login(self):
        response = self.c.post('/auth/register/',
                               {'username': 'vasya',
                                'password1': '111',
                                'password2': '111'})
        self.assertEqual(response.status_code, 302)

        response = self.c.post('/auth/login/',
                               {'username': 'vasya',
                                'password': '111'})
        self.assertEqual(response.status_code, 302)

        response = self.c.post('/auth/login/',
                               {'username': 'fake',
                                'password': 'fake'})
        self.assertEqual(response.status_code, 200)

    def test_create_group(self):
        students = Student.objects.all()
        self.assertEqual(len(students), 0)

        groups = Group.objects.all()
        self.assertEqual(len(groups), 0)

        response = self.c.post('/changing_data/groups/creation/1/',
                               {'name_group': 'C33'})
        self.assertEqual(response.status_code, 302)

        groups = Group.objects.all()
        self.assertEqual(len(groups), 1)

        group_id = Group.objects.get(name_group='C33').id
        new_stu = {
            'student_name': 'Robin Good',
            'dob': '1160-08-20',
            'student_ticket_number': '12800'
        }
        url = '/changing_data/student/creation/' + str(group_id) + '/'
        response = self.c.post(url, new_stu)
        self.assertEqual(response.status_code, 302)

        students = Student.objects.all()
        self.assertEqual(len(students), 1)
