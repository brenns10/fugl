from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=50000)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    project = models.ForeignKey('Project')
    category = models.ForeignKey('Category')
    tags = models.ManyToManyField('Tag')
    post_plugins = models.ManyToManyField('PagePlugin')

    @property
    def filename(self):
        return (slugify(self.title) + '.md')

    def get_markdown(self):
        template = """Title: %(title)s
Author: %(author)s
Date: %(date)s
Modified: %(modified)s

%(content)s
"""
        return (template % {
            'title': self.title,
            'author': self.project.owner.username,
            'date': str(self.date_created),
            'modified': str(self.date_updated),
            'content': self.content,
        })
