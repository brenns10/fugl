
from multiprocessing.pool import ThreadPool
from collections import OrderedDict

from django.core.management.base import BaseCommand
from django.utils import timezone
from tswift import Song

from main.models import User, Project, Post, Page, Category, Theme

artist = 'taylor-swift'
albums = OrderedDict([
    ('1989', [
        'welcome-to-new-york',
        'blank-space',
        'style',
        'out-of-the-woods',
        'all-you-had-to-do-was-stay',
        'shake-it-off',
        'i-wish-you-would',
        'bad-blood',
        'wildest-dreams',
        'how-you-get-the-girl',
        'this-love',
        'i-know-places',
        'clean',
    ]),
    ('Red', [
        'state-of-grace',
        'red',
        'treacherous',
        'i-knew-you-were-trouble',
        'all-too-well',
        '22',
        'i-almost-do',
        'we-are-never-ever-getting-back-together',
        'stay-stay-stay',
        'the-last-time',
        'holy-ground',
        'sad-beautiful-tragic',
        'the-lucky-one',
        'everything-has-changed',
        'starlight',
        'begin-again',
    ]),
    ('Speak Now', [
        'mine',
        'sparks-fly',
        'speak-now',
        'back-to-december',
        'the-story-of-us',
        'innocent',
        'dear-john',
        'mean',
        'never-grow-up',
        'enchanted',
        'better-than-revenge',
        'haunted',
        'last-kiss',
        'long-live',
    ]),
    ('Fearless', [
        'fearless',
        'fifteen',
        'love-story',
        'hey-stephen',
        'white-horse',
        'you-belong-with-me',
        'breathe',
        'tell-me-why',
        'youre-not-sorry',
        'the-way-i-loved-you',
        'forever-always',
        'the-best-day',
        'change',
    ]),
    ('Taylor Swift', [
        'tim-mcgraw',
        'picture-to-burn',
        'teardrops-on-my-guitar',
        'a-place-in-this-world',
        'cold-as-you',
        'the-outside',
        'tied-together-with-a-smile',
        'stay-beautiful',
        'shouldve-said-no',
        'marys-song-oh-my-my-my',
        'our-song',
    ]),
])

username = 'taytay'
password = 'taytay'
email = 'taylor@taylorswift.com'

project_title = 'TSwizzle'
desc = 'taylor swift lyrics'
about = """
Welcome to TSwizzle! This is a site all about TayTay's lyrics. Check out the links above to browse through the available songs.

Also, follow [@pyswizzle](https://twitter.com/pyswizzle) on Twitter.
"""


class Command(BaseCommand):

    args = ''
    help = 'create a project for taylor swift'

    def _get_user(self):
        try:
            return User.objects.get(username=username)
        except:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email)
            user.save()
            return user

    def _get_project(self, user):
        try:
            project = Project.objects.get(title=project_title, owner=user)
        except:
            theme = Theme.objects.get(title='default')
            project = Project.objects.create(title=project_title,
                                             description=desc,
                                             theme=theme,
                                             owner=user)
            project.save()
        project.page_set.all().delete()
        project.post_set.all().delete()
        project.category_set.all().delete()
        page = Page.objects.create(title='About', content=about,
                                   project=project)
        page.save()
        return project

    def _load_lyrics(self, songdict):
        total = []
        for songlist in songdict.values():
            total += songlist

        pool = ThreadPool()
        pool.map(Song.load, total)

    def handle(self, *args, **kwargs):
        user = self._get_user()
        project = self._get_project(user)
        songdict = {a: [Song(artist=artist, title=t) for t in v]
                    for a, v in albums.items()}
        self._load_lyrics(songdict)

        for album, songlist in songdict.items():
            category = Category.objects.create(title=album, project=project)
            category.save()
            for song in songlist:
                lyriclines = song.lyrics.splitlines()
                lyriclines = [l + '  ' for l in lyriclines]
                post = Post.objects.create(title=song._title,
                                           content='\n'.join(lyriclines),
                                           category=category,
                                           project=project,
                                           date_created=timezone.now(),
                                           date_updated=timezone.now())
                post.save()
