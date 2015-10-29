"""
Test for main.views.user.UserHomeView.
"""

from django.test import Client
from main.tests.base import CorvidTestCase


class UserHomeViewTestCase(CorvidTestCase):

    def setUp(self):
        super().setUpTheme()
        self.client = Client()

    def tearDown(self):
        super().tearDownTheme()

    def test_not_logged_in_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_logged_in_go_to_home(self):
        self.assertTrue(self.client.login(username=self.admin_user.username,
                                          password=self.admin_password))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/home/', response.url)
