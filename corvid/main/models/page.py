from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=50000)

    post_plugins = models.ManyToManyField('PagePlugin')
