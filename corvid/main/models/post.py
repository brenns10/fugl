from django.db import models
from django.utils.text import slugify

from main.models import Category


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=50000)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    project = models.ForeignKey('Project')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    post_plugins = models.ManyToManyField('PagePlugin')

    @property
    def filename(self):
        return slugify(self.title)

    def get_markdown(self, slug=None):
        kwargs = {
            'title': self.title,
            'author': self.project.owner.username,
            'content': self.content,
            'date_created_str': '',
            'date_modified_str': '',
            'slug': slug if slug else self.title,
        }
        date_fmt = '%Y-%m-%d'
        if self.date_created is not None:
            kwargs['date_created_str'] = ('Date: {0}\n'
                                          .format(self.date_created.strftime(date_fmt)))
        if self.date_updated is not None:
            kwargs['date_modified_str'] = ('Modified: {0}\n'
                                           .format(self.date_updated.strftime(date_fmt)))
        return (post_template % kwargs)

    def clone(self, newproject, plugins):
        category = Category.objects.get(project=newproject,
                                        title=self.category.title)
        kwargs = {
            'title': self.title,
            'content': self.content,
            'date_created': self.date_created,
            'date_updated': self.date_updated,
            'project': newproject,
            'category': category,
        }
        new = Post.objects.create(**kwargs)

        if plugins:
            for plugin in self.post_plugins.all():
                new.post_plugins.add(plugins[plugin])

        new.save()
        return new


post_template = """Title: %(title)s
Author: %(author)s
Slug: %(slug)s
%(date_created_str)s%(date_modified_str)s
%(content)s
"""
