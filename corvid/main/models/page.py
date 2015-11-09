from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    post_plugins = models.ManyToManyField('PagePlugin')
    project = models.ForeignKey('Project')
