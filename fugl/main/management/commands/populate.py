from django.core.management.base import BaseCommand, CommandError
from os.path import isdir, abspath, join
from os import listdir
from main.models import User, Theme


class Command(BaseCommand):
    args = ''
    help = 'Populate database with default objects'

    def add_arguments(self, parser):
        parser.add_argument('theme_dir', type=str,
                            help='directory containing themes')

    def handle(self, *args, **kwargs):
        ADMIN_USERNAME = 'admin_user'
        admin_user = User.objects.create_user(ADMIN_USERNAME,
                                              'admin@example.com',
                                              'cock-of-the-rock')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.is_active = True
        admin_user.save()

        theme_dir = kwargs['theme_dir']

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
