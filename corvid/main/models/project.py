"""
Represents a project: a static website.
"""
from django.db import models
from .user import User


class Project(models.Model):
    """
    Represents a project: a static website
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    preview_url = models.URLField()

    owner = models.ForeignKey(User)
    theme = models.ForeignKey('Theme')

    @property
    def project_home_url(self):
        return '/project/{0}'.format(self.preview_url)

    def get_pelican_conf(self, content_path='content'):
        """Returns pelicanconf correspnding to this Project."""
        template_args = {
            'author': self.owner.username,
            'site_name': self.title,
            'content_path': content_path,
        }
        return pelicanconf_template % template_args


pelicanconf_template = """#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = '%(author)s'
SITENAME = '%(site_name)s'
SITEURL = ''

PATH = '%(content_path)s'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
"""
