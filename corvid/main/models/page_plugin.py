from django.db import models


class PagePlugin(models.Model):
    class Meta:
        unique_together = (('title', 'project'),)
        index_together = (('title', 'project'),)

    title = models.CharField(max_length=50)
    head_markup = models.TextField(max_length=5000)
    body_markup = models.TextField(max_length=5000)

    project = models.ForeignKey('Project')

    def clone(self, newproject):
        """Clone the plugin into a new project."""
        kwargs = {
            'title': self.title,
            'head_markup': self.head_markup,
            'body_markup': self.body_markup,
            'project': newproject,
        }
        new = PagePlugin.objects.create(**kwargs)
        new.save()
        return new
