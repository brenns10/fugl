from django.core.management.base import BaseCommand, CommandError
from os.path import isdir, abspath, join
from os import listdir
from main.models import User, Theme

ADMIN_USERNAME = 'admin_user'


class Command(BaseCommand):
    args = ''
    help = 'Populate database with themes'

    def add_arguments(self, parser):
        parser.add_argument('theme_dir', type=str,
                            help='directory containing themes')

    def handle(self, *args, **kwargs):
        theme_dir = kwargs['theme_dir']

        # Check to make sure you have populated and gotten an admin.
        admin_users = User.objects.filter(username=ADMIN_USERNAME)
        if len(admin_users) != 1:
            raise CommandError('You have not yet run ./manage.py populate.')
        admin_user = admin_users[0]

        # Make sure it's a valid directory.
        if not isdir(theme_dir):
            raise CommandError('Theme directory does not exist!')

        theme_path = abspath(theme_dir)

        # Create a name -> fullpath dict of themes.
        themes = {}
        for d in listdir(theme_path):
            full = join(theme_path, d)
            if isdir(full):
                themes[d] = full  # TODO: come up with better names than d

        for name, path in themes.items():
            print('Registering theme %s.' % name)
            theme = Theme.objects.create(title=name, filepath=path,
                                         creator=admin_user)
            theme.save()
