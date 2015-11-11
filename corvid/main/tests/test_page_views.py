"""
Tests for main.views.page classes: CreatePageView and UpdatePageView.
"""

from django.test import Client
from .base import CorvidTestCase


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
