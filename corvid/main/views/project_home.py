from django.views.generic.detail import DetailView
from .protected_view import ProtectedViewMixin
from main.models.user import User
from main.models.project import Project
from main.models.page import Page
from main.models.category import Category


class ProjectDetailView(DetailView, ProtectedViewMixin):
    model = Project
    template_name = 'project_home.html'

    def get_object(self):
        owner = User.objects.get(username=self.kwargs['owner'])
        kwargs = {
            'owner': owner,
            'title': self.kwargs['title'],
        }
        return Project.objects.get(**kwargs)

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
