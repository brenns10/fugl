"""
Tests for main.views.page classes: CreatePageView and UpdatePageView.

Tests:
CreatePageView:
- GET:
  - not logged in user redirected to login.
  - logged in user cannot access form to create a page for projects they don't
    own. (should 404)
  - logged in user can access form to create a page for projects they do own.
- POST:
  - not logged in user redirected to login
  - logged in user may not create page on project they don't own (should 404)
  - logged in user can create a page for project they do own (expected case)
UpdatePageView:
- GET:
  - not logged in user redirected to login
  - logged in user cannot access page for project they don't own (should 404)
  - logged in user can access page for project they do own
    -> should return the page's existing content
- POST:
  - not logged in user redirected to login
  - logged in user cannot edit page for project they don't own (should 404)
  - logged in user can edit page contents
    - should be reflected in database
"""

from django.test import Client
from .base import CorvidTestCase
from main.models.page import Page
from main.models.user import User
from main.models.project import Project


class CreatePageViewTestCase(CorvidTestCase):

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
        self.page.delete()
        self.project.delete()
        super().tearDownTheme()

    def url_for(self, project):
        # return the url for a project
        return '/project/%s/%s/page/new' % (project.owner.username,
                                            project.title)

    def login_other(self):
        # login the client as "otheruser"
        self.client.login(username=self.otheruser.username,
                          password=self.otherpass)

    def test_get_not_logged_in_redirect(self):
        # When a not-logged-in user accesses the page, it should redirect.
        url = self.url_for(self.project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next='+url)

    def test_get_not_owner_404(self):
        # Should 404 if you don't own the project
        url = self.url_for(self.project)
        self.login_other()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_owner(self):
        # Should return the correct form when you own the project
        url = self.url_for(self.project)
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Create Page', response.content)

    def test_post_not_logged_in_redirect(self):
        url = self.url_for(self.project)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next='+url)

    def test_post_not_owner_404(self):
        # Should 404 if you don't own the project
        url = self.url_for(self.project)
        self.login_other()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_post_owner(self):
        formdata = {'title':'testpage2', 'content': 'I am a test page.'}
        url = self.url_for(self.project)
        self.login()
        response = self.client.post(url, formdata)
        self.assertEqual(response.status_code, 200)

        # Also, there should be a corresponding page object in the DB.
        page_object = Page.objects.get(project=self.project,
                                       title=formdata['title'])
        self.assertEqual(page_object.content, formdata['content'])

        # Cleanup before the test is over.
        page_object.delete()


class CreatePageViewTestCase(CorvidTestCase):

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

        self.page = Page.objects.create(
            title='testpage1', content='test page 1', project=self.project)
        self.page.save()

    def tearDown(self):
        self.otheruser.delete()
        self.page.delete()
        self.project.delete()
        super().tearDownTheme()

    def url_for(self, page):
        # return the url for a project
        return '/project/%s/%s/page/edit/%s' % (page.project.owner.username,
                                                page.project.title,
                                                page.title)

    def login_other(self):
        # login the client as "otheruser"
        self.client.login(username=self.otheruser.username,
                          password=self.otherpass)

    def test_get_not_logged_in_redirect(self):
        # When a not-logged-in user accesses the page, it should redirect.
        url = self.url_for(self.page)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next='+url)

    def test_get_not_owner_404(self):
        # Should 404 if you don't own the project
        url = self.url_for(self.page)
        self.login_other()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_owner(self):
        # Should return the correct form when you own the project
        url = self.url_for(self.page)
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf8')
        self.assertIn('Edit Page', content)
        self.assertIn(self.page.content, content)
        self.assertIn(self.page.title, content)

    def test_post_not_logged_in_redirect(self):
        url = self.url_for(self.page)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/login/?next='+url)

    def test_post_not_owner_404(self):
        # Should 404 if you don't own the project
        url = self.url_for(self.page)
        self.login_other()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_post_owner(self):
        # Data we will send in the form
        newdata = {
            'title': self.page.title,
            'content': 'new content',
        }

        # Post to the form.
        self.login()
        url = self.url_for(self.page)
        response = self.client.post(url, newdata)

        # Assert that it redirects to the project home.
        self.assertEqual(response.status_code, 302)
        redir_url = '/project/%s/%s'  % (self.admin_user.username,
                                         self.project.title)
        redir_url = 'http://testserver' + redir_url
        self.assertIn(redir_url, response.url)

        # Assert that the change happened.
        self.page.refresh_from_db()
        self.assertEqual(self.page.content, newdata['content'])
