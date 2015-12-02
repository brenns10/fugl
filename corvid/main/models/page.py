from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=50000)

    post_plugins = models.ManyToManyField('PagePlugin')
    project = models.ForeignKey('Project')

    @property
    def filename(self):
        return slugify(self.title)

    def get_markdown(self, slug=None):
        return (page_template % {
            'title': self.title,
            'content': self.content,
            'slug': slug if slug else self.title
        })

    def clone(self, newproject, plugins):
        kwargs = {
            'title': self.title,
            'content': self.content,
            'project': newproject,
        }
        new = Page.objects.create(**kwargs)

        if plugins:
            for plugin in self.post_plugins.all():
                new.post_plugins.add(plugins[plugin])

        new.save()
        return new


page_template = """Title: %(title)s
Slug: %(slug)s

%(content)s
"""
