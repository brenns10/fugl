from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .project_home import ProtectedViewMixin
from main.models import User, Project


class ProjectSettingsView(ProtectedViewMixin, UpdateView):

    template_name = 'choose_theme.html'
    model = Project
    fields = ['theme']

    def get_object(self):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        projectqs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(projectqs, owner=user,
                                    title=self.kwargs['title'])
        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.title
        context['current_theme'] = self.object.theme.title
        return context

    def get_success_url(self):
        kwargs = {
            'owner': self.object.owner.username,
            'title': self.object.title,
        }
        return reverse('project_home', kwargs=kwargs)
