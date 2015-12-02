"""
Tests for cloning projects.
"""

from django.utils import timezone

from .base import CorvidTestCase
from main.models import (Project, Page, Post, Category, Theme, ProjectPlugin,
                         PagePlugin)


class CloneProjectTestCase(CorvidTestCase):

    def setUp(self):
        super().setUpTheme()

        # A "new theme" so we can test theme cloning.
        self.other_theme = Theme.objects.create(title='other',
                                                filepath='html5dopetrope',
                                                creator=self.admin_user)
        self.other_theme.save()

        # A project to clone.
        self.project = Project.objects.create(
            title='project', description='test project', preview_url='',
            owner=self.admin_user, theme=self.other_theme
        )
        self.project.save()

        # Some plugins
        self.page_plugin = PagePlugin.objects.create(
            title='page plugin', head_markup='<script>alert("hi")</script>',
            body_markup='<h1>I\'m a plugin!</h1>', project=self.project
        )
        self.page_plugin.save()

        self.project_plugin = ProjectPlugin.objects.create(
            title='project plugin',
            markup='<script>alert("project_plugin")</script>',
            project=self.project
        )
        self.project_plugin.save()

        # Some categories
        self.category_one = Category.objects.create(
            title='category1', project=self.project
        )
        self.category_one.save()

        self.category_two = Category.objects.create(
            title='category2', project=self.project
        )
        self.category_two.save()

        # And some pages and posts
        self.page_one = Page.objects.create(
            title='Home',
            content='Welcome to the test project (it\'s been waiting for you)',
            project=self.project
        )
        self.page_one.save()
        self.page_one.post_plugins.add(self.page_plugin)
        self.page_one.save()  # probably unnecessary

        self.page_two = Page.objects.create(
            title='About', content='I\'m a page!', project=self.project
        )
        self.page_one.save()

        self.post_one = Post.objects.create(
            title='First Post',
            content='Do you have a moment to talk about our lord and Savior, '
            'Pelican?',
            project=self.project, category=self.category_one,
            date_created=timezone.now(), date_updated=timezone.now()
        )
        self.post_one.save()
        self.post_one.post_plugins.add(self.page_plugin)
        self.post_one.save()  # probably unnecessary

        self.post_two = Post.objects.create(
            title='Second Post', content='I\'m a post!', project=self.project,
            category=self.category_two, date_created=timezone.now(),
            date_updated=timezone.now()
        )
        self.post_one.save()

    def tearDown(self):
        super().tearDownTheme()

    def test_clone_nothing(self):
        new = self.project.clone('cloned', False, False, False, False)
        # Assert that attributes were cloned properly.
        self.assertEqual(new.title, 'cloned')
        self.assertEqual(new.description, self.project.description)
        self.assertEqual(new.preview_url, self.project.preview_url)
        self.assertEqual(new.owner, self.project.owner)

        # Categories are cloned
        self.assertEqual(new.category_set.count(), 2)
        self.assertEqual(new.category_set.filter(title=self.category_one.title).count(), 1)
        self.assertEqual(new.category_set.filter(title=self.category_two.title).count(), 1)

        # Assert that the theme was not cloned.
        self.assertNotEqual(new.theme, self.project.theme)
        self.assertEqual(new.theme, self.default_theme)

        # Assert that the pages, posts, and plugins were not cloned.
        self.assertEqual(new.page_set.count(), 0)
        self.assertEqual(new.post_set.count(), 0)
        self.assertEqual(new.pageplugin_set.count(), 0)
        self.assertEqual(new.projectplugin_set.count(), 0)

    def test_clone_theme(self):
        new = self.project.clone('cloned', True, False, False, False)
        # Assert that attributes were cloned properly.
        self.assertEqual(new.title, 'cloned')
        self.assertEqual(new.description, self.project.description)
        self.assertEqual(new.preview_url, self.project.preview_url)
        self.assertEqual(new.owner, self.project.owner)

        # Categories are cloned
        self.assertEqual(new.category_set.count(), 2)
        self.assertEqual(new.category_set.filter(title=self.category_one.title).count(), 1)
        self.assertEqual(new.category_set.filter(title=self.category_two.title).count(), 1)

        # Assert that the theme was cloned.
        self.assertEqual(new.theme, self.project.theme)

        # Assert that the pages, posts, and plugins were not cloned.
        self.assertEqual(new.page_set.count(), 0)
        self.assertEqual(new.post_set.count(), 0)
        self.assertEqual(new.pageplugin_set.count(), 0)
        self.assertEqual(new.projectplugin_set.count(), 0)

    def test_clone_pages(self):
        new = self.project.clone('cloned', False, True, False, False)
        # Assert that attributes were cloned properly.
        self.assertEqual(new.title, 'cloned')
        self.assertEqual(new.description, self.project.description)
        self.assertEqual(new.preview_url, self.project.preview_url)
        self.assertEqual(new.owner, self.project.owner)

        # Categories are cloned
        self.assertEqual(new.category_set.count(), 2)
        self.assertEqual(new.category_set.filter(title=self.category_one.title).count(), 1)
        self.assertEqual(new.category_set.filter(title=self.category_two.title).count(), 1)

        # Assert that the theme was not cloned.
        self.assertNotEqual(new.theme, self.project.theme)
        self.assertEqual(new.theme, self.default_theme)

        # Assert that the posts and plugins were not cloned.
        self.assertEqual(new.post_set.count(), 0)
        self.assertEqual(new.pageplugin_set.count(), 0)
        self.assertEqual(new.projectplugin_set.count(), 0)

        # Assert that the pages were cloned.
        self.assertEqual(new.page_set.count(), 2)
        p1 = new.page_set.get(title=self.page_one.title)
        self.assertEqual(p1.title, self.page_one.title)
        self.assertEqual(p1.content, self.page_one.content)
        self.assertEqual(p1.project, new)
        p2 = new.page_set.get(title=self.page_two.title)
        self.assertEqual(p2.title, self.page_two.title)
        self.assertEqual(p2.content, self.page_two.content)
        self.assertEqual(p2.project, new)

        # Since the plugins were not cloned, p1 and p2 will not have any!
        self.assertEqual(p1.post_plugins.count(), 0)
        self.assertEqual(p2.post_plugins.count(), 0)

    def test_clone_posts(self):
        new = self.project.clone('cloned', False, False, True, False)
        # Assert that attributes were cloned properly.
        self.assertEqual(new.title, 'cloned')
        self.assertEqual(new.description, self.project.description)
        self.assertEqual(new.preview_url, self.project.preview_url)
        self.assertEqual(new.owner, self.project.owner)

        # Assert that the theme was not cloned.
        self.assertNotEqual(new.theme, self.project.theme)
        self.assertEqual(new.theme, self.default_theme)

        # Assert that the pages and plugins were not cloned.
        self.assertEqual(new.page_set.count(), 0)
        self.assertEqual(new.pageplugin_set.count(), 0)
        self.assertEqual(new.projectplugin_set.count(), 0)

        # Assert that the posts were cloned.
        self.assertEqual(new.post_set.count(), 2)
        p1 = new.post_set.get(title=self.post_one.title)
        self.assertEqual(p1.title, self.post_one.title)
        self.assertEqual(p1.content, self.post_one.content)
        self.assertEqual(p1.date_created, self.post_one.date_created)
        self.assertEqual(p1.date_updated, self.post_one.date_updated)
        self.assertNotEqual(p1.category, self.post_one.category)
        self.assertEqual(p1.category.title, self.post_one.category.title)
        self.assertEqual(p1.project, new)
        p2 = new.post_set.get(title=self.post_two.title)
        self.assertEqual(p2.title, self.post_two.title)
        self.assertEqual(p2.content, self.post_two.content)
        self.assertEqual(p2.date_created, self.post_two.date_created)
        self.assertEqual(p2.date_updated, self.post_two.date_updated)
        self.assertNotEqual(p2.category, self.post_two.category)
        self.assertEqual(p2.category.title, self.post_two.category.title)
        self.assertEqual(p2.project, new)

        # Since plugins weren't cloned, none of them have plugins.
        self.assertEqual(p1.post_plugins.count(), 0)
        self.assertEqual(p2.post_plugins.count(), 0)

    def test_clone_plugins(self):
        new = self.project.clone('cloned', False, False, False, True)
        # Assert that attributes were cloned properly.
        self.assertEqual(new.title, 'cloned')
        self.assertEqual(new.description, self.project.description)
        self.assertEqual(new.preview_url, self.project.preview_url)
        self.assertEqual(new.owner, self.project.owner)

        # Categories are cloned
        self.assertEqual(new.category_set.count(), 2)
        self.assertEqual(new.category_set.filter(title=self.category_one.title).count(), 1)
        self.assertEqual(new.category_set.filter(title=self.category_two.title).count(), 1)

        # Assert that the theme was not cloned.
        self.assertNotEqual(new.theme, self.project.theme)
        self.assertEqual(new.theme, self.default_theme)

        # Assert that the pages and posts were not cloned.
        self.assertEqual(new.page_set.count(), 0)
        self.assertEqual(new.post_set.count(), 0)

        # Assert that plugins are cloned.
        self.assertEqual(new.pageplugin_set.count(), 1)
        p = new.pageplugin_set.get(title=self.page_plugin.title)
        self.assertEqual(p.head_markup, self.page_plugin.head_markup)
        self.assertEqual(p.body_markup, self.page_plugin.body_markup)
        self.assertEqual(p.project, new)
        self.assertEqual(new.projectplugin_set.count(), 1)
        p = new.projectplugin_set.get(title=self.project_plugin.title)
        self.assertEqual(p.markup, self.project_plugin.markup)
        self.assertEqual(p.project, new)

    def test_clone_all(self):
        new = self.project.clone('cloned', True, True, True, True)
        # Assert that attributes were cloned properly.
        self.assertEqual(new.title, 'cloned')
        self.assertEqual(new.description, self.project.description)
        self.assertEqual(new.preview_url, self.project.preview_url)
        self.assertEqual(new.owner, self.project.owner)

        # Assert that the theme was cloned.
        self.assertEqual(new.theme, self.project.theme)

        # Assert that plugins are cloned.
        self.assertEqual(new.pageplugin_set.count(), 1)
        p = new.pageplugin_set.get(title=self.page_plugin.title)
        self.assertEqual(p.head_markup, self.page_plugin.head_markup)
        self.assertEqual(p.body_markup, self.page_plugin.body_markup)
        self.assertEqual(p.project, new)
        self.assertEqual(new.projectplugin_set.count(), 1)
        p = new.projectplugin_set.get(title=self.project_plugin.title)
        self.assertEqual(p.markup, self.project_plugin.markup)
        self.assertEqual(p.project, new)

        # Assert that the pages were cloned.
        self.assertEqual(new.page_set.count(), 2)
        p1 = new.page_set.get(title=self.page_one.title)
        self.assertEqual(p1.title, self.page_one.title)
        self.assertEqual(p1.content, self.page_one.content)
        self.assertEqual(p1.project, new)
        p2 = new.page_set.get(title=self.page_two.title)
        self.assertEqual(p2.title, self.page_two.title)
        self.assertEqual(p2.content, self.page_two.content)
        self.assertEqual(p2.project, new)
        # Since the plugins were cloned, they will have the same amount
        self.assertEqual(p1.post_plugins.count(), self.page_one.post_plugins.count())
        self.assertEqual(p2.post_plugins.count(), self.page_two.post_plugins.count())

        # Assert that the posts were cloned.
        self.assertEqual(new.post_set.count(), 2)
        p1 = new.post_set.get(title=self.post_one.title)
        self.assertEqual(p1.title, self.post_one.title)
        self.assertEqual(p1.content, self.post_one.content)
        self.assertEqual(p1.date_created, self.post_one.date_created)
        self.assertEqual(p1.date_updated, self.post_one.date_updated)
        self.assertNotEqual(p1.category, self.post_one.category)
        self.assertEqual(p1.category.title, self.post_one.category.title)
        self.assertEqual(p1.project, new)
        p2 = new.post_set.get(title=self.post_two.title)
        self.assertEqual(p2.title, self.post_two.title)
        self.assertEqual(p2.content, self.post_two.content)
        self.assertEqual(p2.date_created, self.post_two.date_created)
        self.assertEqual(p2.date_updated, self.post_two.date_updated)
        self.assertNotEqual(p2.category, self.post_two.category)
        self.assertEqual(p2.category.title, self.post_two.category.title)
        self.assertEqual(p2.project, new)
        # Since plugins were cloned, they will have the same amount.
        self.assertEqual(p1.post_plugins.count(), self.post_one.post_plugins.count())
        self.assertEqual(p2.post_plugins.count(), self.post_two.post_plugins.count())

