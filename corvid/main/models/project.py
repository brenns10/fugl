"""
Represents a project: a static website.
"""
from django.db import models
from user import User


class Project(models.Model):
    """
    Represents a project: a static website
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    preview_url = models.URLField()

    owner = models.ForeignKey(User)
    theme = models.ForeignKey('Theme')
