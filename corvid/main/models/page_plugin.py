from django.db import models


class PagePlugin(models.Model):
    class Meta:
        unique_together = (('title', 'project'),)
        index_together = (('title', 'project'),)

    title = models.CharField(max_length=50)
    head_markup = models.CharField(max_length=5000)
    body_markup = models.CharField(max_length=5000)

    project = models.ForeignKey('Project')
