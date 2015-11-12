"""
Tests for main.views.page classes: CreatePageView and UpdatePageView.
"""

from django.test import Client
from .base import CorvidTestCase
from main.models import Page, User, Project


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
        self.project.delete()
        super().tearDownTheme()

    def test_create_page(self):
        formdata = {'title':'test_page1', 'content': 'I am a test page.'}
        url = '/project/%s/%s/page/new' % (self.admin_user.username,
                                           self.project.title)
        self.client.login(username=self.admin_user.username,
                          password=self.admin_password)
        response = self.client.post(url, formdata)

        # On success, the page should return 200.
        self.assertEqual(response.status_code, 200)

        # Also, there should be a corresponding page object in the DB.
        page_object = Page.objects.get(project=self.project,
                                       title=formdata['title'])
        self.assertEqual(page_object.content, formdata['content'])

        # Cleanup before the test is over.
        page_object.delete()

    def test_update_page(self):
        # First, create a page and save it to the database.
        data = {
            'title': 'CreatePageViewTestCase.test_update_page',
            'content': 'original content',
            'project': self.project
        }
        page = Page.objects.create(**data)
        page.save()
        self.assertEqual(page.content, data['content'])

        # Now, we will update it using the update page view.
        del data['project']
        data['content'] = 'new content'

        # Stuff to send the response.
        self.client.login(username=self.admin_user.username,
                          password=self.admin_password)
        url = '/project/%s/%s/page/edit/%s' % (self.admin_user.username,
                                               self.project.title,
                                               data['title'])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        redir_url = '/project/%s/%s'  % (self.admin_user.username,
                                         self.project.title)
        self.assertIn(redir_url, response.url)

        # Get an updated version of the page, and make sure the change occurred.
        page = Page.objects.get(project=self.project, title=data['title'])
        self.assertEqual(page.content, data['content'])
        page.delete()
