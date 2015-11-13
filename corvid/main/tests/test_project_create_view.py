"""
Tests for main.views.create_project class: CreateProjectView

Tests:
GET:
- not logged in user redirected to login
- user can access form
POST:
- not logged in user redirected to login
- user can create project
  - empty project name?
  - empty description?
  - invalid names?
"""

from django.test import Client
from .base import CorvidTestCase
from main.models import Project


class CreateProjectViewTestCase(CorvidTestCase):

    def setUp(self):
        super().setUpTheme()
        self.client = Client()

    def tearDown(self):
        super().tearDownTheme()

    url = '/project/create'

    def test_get_not_logged_in_redirect(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, 'http://testserver/login/?next=' + self.url)

    def test_get_logged_in(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Create Project', resp.content)

    def test_post_not_logged_in_redirect(self):
        data = {'title': 'blah', 'description': 'blah project'}
        resp = self.client.post(self.url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, 'http://testserver/login/?next=' + self.url)

    def test_post_logged_in(self):
        data = {'title': 'blah', 'description': 'blah project'}
        self.login()
        resp = self.client.post(self.url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Project created!', resp.content)
        project_list = Project.objects.filter(owner=self.admin_user,
                                              title=data['title'])
        self.assertEqual(len(project_list), 1)
        project_list[0].delete()

    def test_empty_project_name(self):
        old_number_of_projects = len(Project.objects.all())
        data = {'title': '', 'description': 'blah project'}
        self.login()
        resp = self.client.post(self.url, data)
        # 200 doesn't mean failure, sadly
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'This field is required.', resp.content)
        new_number_of_projects = len(Project.objects.all())
        self.assertEqual(old_number_of_projects, new_number_of_projects)
