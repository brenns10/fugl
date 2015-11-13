"""
Tests for main.views.category class: CreateCategoryView.

Tests:
GET:
- not logged in user redirected to login
- non-owner cannot access form (404)
- owner can access form
POST:
- not logged in user redirected to login
- non-owner cannot post (404)
- owner can create category
"""

from django.test import Client
from .base import CorvidTestCase
from main.models import User, Project, Category


class CreateCategoryViewTestCase(CorvidTestCase):

    def setUp(self):
        super().setUpTheme()
        self.client = Client()
        self.otherpass = 'cock-of-the-rock'
        self.otheruser = User.objects.create_user('other_user',
                                                  'other@example.com',
                                                  self.otherpass)
        self.otheruser.save()
        self.project = Project.objects.create(
            title='testproj', description='test project', preview_url='',
            owner=self.admin_user, theme=self.default_theme
        )
        self.project.save()

    def tearDown(self):
        self.otheruser.delete()
        self.project.delete()
        super().tearDownTheme()

    def url_for(self, project):
        # return the "new category" url for a project
        return '/project/%s/%s/category/new' % (project.owner.username,
                                                project.title)

    def login_other(self):
        # login the client as "otheruser"
        self.client.login(username=self.otheruser.username,
                          password=self.otherpass)

    def test_get_not_logged_in_redirect(self):
        url = self.url_for(self.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next=' + url)

    def test_get_not_owner_404(self):
        url = self.url_for(self.project)
        self.login_other()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_owner(self):
        url = self.url_for(self.project)
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_not_logged_in_redirect(self):
        url = self.url_for(self.project)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next=' + url)

    def test_post_not_owner_404(self):
        url = self.url_for(self.project)
        self.login_other()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_post_owner(self):
        url = self.url_for(self.project)
        data = {'title': 'Serious Business'}
        self.login()
        response = self.client.post(url, data)
        # should get redirected to the project home
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Category created!', response.content)
        cats = Category.objects.filter(project=self.project,
                                       title=data['title'])
        self.assertEqual(len(cats), 1)
        cats[0].delete()

    def test_get_invalid_user(self):
        url = '/project/idontexist/%s/category/new' % self.project.title
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_invalid_user(self):
        url = '/project/idontexist/%s/category/new' % self.project.title
        data = {'title': 'Serious Business'}
        self.login()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

    def test_get_invalid_project(self):
        url = '/project/%s/doesntexist/category/new' % self.admin_user.username
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_invalid_project(self):
        url = '/project/%s/doesntexist/category/new' % self.admin_user.username
        data = {'title': 'Serious Business'}
        self.login()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
