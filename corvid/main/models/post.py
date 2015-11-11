from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=50000)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    project = models.ForeignKey('Project')
    category = models.ForeignKey('Category')
    tags = models.ManyToManyField('Tag')
    post_plugins = models.ManyToManyField('PagePlugin')
