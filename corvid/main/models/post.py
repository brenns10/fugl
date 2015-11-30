from django.db import models
from django.utils.text import slugify


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
        return (slugify(self.title) + '.md')

    def get_markdown(self):
        kwargs = {
            'title': self.title,
            'author': self.project.owner.username,
            'content': self.content,
            'date_created_str': '',
            'date_modified_str': '',
        }
        date_fmt = '%Y-%m-%d'
        if self.date_created is not None:
            kwargs['date_created_str'] = ('Date: {0}\n'
                                          .format(self.date_created.strftime(date_fmt)))
        if self.date_updated is not None:
            kwargs['date_modified_str'] = ('Modified: {0}\n'
                                           .format(self.date_updated.strftime(date_fmt)))
        return (post_template % kwargs)


post_template = """Title: %(title)s
Author: %(author)s
%(date_created_str)s%(date_modified_str)s
%(content)s
"""
