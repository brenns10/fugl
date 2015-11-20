from django.db import models
from .user import User


class Theme(models.Model):
    title = models.CharField(max_length=50, unique=True)
    filepath = models.FilePathField()
    body_markup = models.CharField(max_length=5000)

    creator = models.ForeignKey(User)

    def __str__(self):
        return self.title
