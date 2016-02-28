"""
Where an extension to the base User model lives.

Django's builtin `User` model has `username`, `email`, and `password`
fields (but does not require the email field), so we may not need to
extend the model here.
"""
from django.contrib.auth.models import User
