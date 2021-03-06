from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .protected_view import ProtectedViewMixin
from main.models import Category, Project, User, Page, Post, ProjectPlugin


class ProjectDetailView(ProtectedViewMixin, DetailView):
    model = Project
    template_name = 'project_home.html'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        user = get_object_or_404(User.objects,
                                 username=self.kwargs['owner'])
        return get_object_or_404(queryset, owner=user,
                                 title=self.kwargs['title'])

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['owner'] = self.object.owner.username
        context['title'] = self.object.title
        pages = [p for p in Page.objects.filter(project=self.object)]
        posts = [p for p in Post.objects.filter(project=self.object)]
        project_plugins = [p for p in ProjectPlugin.objects.filter(project=self.object)]
        page_plugins = [p for p in self.object.pageplugin_set.all()]
        context['pages_'] = pages
        context['posts_'] = posts
        context['project_plugins_'] = project_plugins
        context['page_plugins_'] = page_plugins
        categories = Category.objects.filter(project=self.object)
        context['categories'] = [c for c in categories]
        # TODO: Getting posts: Category -> posts
        # context['posts'] = categories.filter(title__in=categories)
        return context
