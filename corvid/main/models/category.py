from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)

    project = models.ForeignKey('Project')

    def __str__(self):
        return self.title
