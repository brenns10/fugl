from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .protected_view import ProtectedViewMixin
from main.models.project import Project
from main.models.user import User
from main.models.page import Page


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
        print(len(pages))
        context['pages_'] = pages
        # TODO: Getting posts: Category -> posts
        # categories = Category.objects.filter(project=self.object)
        # context['posts'] = categories.filter(title__in=categories)
        return context
