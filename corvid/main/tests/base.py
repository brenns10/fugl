"""
Base class for Corvid tests that set up some database stuff.
"""

from django.test import TestCase
from main.models import User, Theme


class CorvidTestCase(TestCase):

    def setUpTheme(self):
        self.admin_password = 'cock-of-the-rock'
        self.admin_user = User.objects.create_user('admin_user',
                                                   'admin@example.com',
                                                   self.admin_password)
        self.admin_user.save()

        self.default_theme = Theme.objects.create(title='default',
                                                  filepath='themes/default',
                                                  body_markup='<script>console.log("")</script>',
                                                  creator=self.admin_user)
        self.default_theme.save()

    def tearDownTheme(self):
        self.default_theme.save()
        self.admin_user.delete()
