from django.core.management.base import BaseCommand
from main.models import User, Theme


class Command(BaseCommand):
    args = ''
    help = 'Populate database with default objects'

    def handle(self, *args, **kwargs):
        admin_user = User.objects.create_user('admin_user',
                                              'admin@example.com',
                                              'cock-of-the-rock')
        admin_user.save()

        default_theme = Theme.objects.create(title='default',
                                             filepath='themes/default',
                                             body_markup='<script>console.log("")</script>',
                                             creator=admin_user)
        default_theme.save()
