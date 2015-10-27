from django.contrib import admin


# Register your models here.
from .models.project import Project
from .models.theme import Theme
from .models.project_plugin import ProjectPlugin
from .models.page import Page
from .models.post import Post
from .models.tag import Tag
from .models.category import Category
from .models.page_plugin import PagePlugin


admin.site.register(Project)
admin.site.register(Theme)
admin.site.register(ProjectPlugin)
admin.site.register(Page)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(PagePlugin)
