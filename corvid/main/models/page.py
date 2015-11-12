from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=50000)

    post_plugins = models.ManyToManyField('PagePlugin')
    project = models.ForeignKey('Project')

    @property
    def filename(self):
        return (slugify(self.title) + '.md')

    def get_markdown(self):
        template = """Title: %(title)s

%(content)s
"""
        return (template % {
            'title': self.title,
            'content': self.content,
        })
