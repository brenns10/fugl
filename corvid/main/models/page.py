from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=50000)

    post_plugins = models.ManyToManyField('PagePlugin')
    project = models.ForeignKey('Project')
