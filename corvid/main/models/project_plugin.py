from django.db import models


class ProjectPlugin(models.Model):
    class Meta:
        unique_together = (('title', 'project'),)
        index_together = (('title', 'project'),)

    title = models.CharField(max_length=50)
    markup = models.TextField(max_length=5000)

    project = models.ForeignKey('Project')
