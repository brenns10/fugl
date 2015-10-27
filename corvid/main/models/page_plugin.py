from django.db import models


class PagePlugin(models.Model):
    title = models.CharField(max_length=50)
    head_markup = models.CharField(max_length=5000)
    body_markup = models.CharField(max_length=5000)

    project = models.ForeignKey('Project')
