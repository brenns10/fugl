from django.db import models


class ProjectPlugin(models.Model):
    title = models.CharField(max_length=50)
    markup = models.CharField(max_length=5000)

    project = models.ForeignKey('Project')
