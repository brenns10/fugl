from django.contrib import admin


# Don't hate on star imports.  Sometimes they're just better.
from .models import *


# Register your models here.
admin.site.register(Project)
admin.site.register(Theme)
admin.site.register(ProjectPlugin)
admin.site.register(Page)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(PagePlugin)
