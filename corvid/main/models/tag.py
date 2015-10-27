from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=50)

    project = models.ForeignKey('Project')
    posts = models.ManyToManyField('Post')
