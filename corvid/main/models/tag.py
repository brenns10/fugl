from django.db import models


class Tag(models.Model):
    class Meta:
        unique_together = (('title', 'project'),)
        index_together = (('title', 'project'),)

    title = models.CharField(max_length=50)

    project = models.ForeignKey('Project')
    posts = models.ManyToManyField('Post')
