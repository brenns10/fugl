from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django import forms
from main.models import Project, User, ProjectPlugin
from .protected_view import ProtectedViewMixin
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django import forms


class ProjectPluginForm(forms.ModelForm):
    class Meta:
        model = ProjectPlugin
        fields = ['title', 'markup']


class ProjectPluginBase(object):
    def get_project(self):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        user_projects = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(user_projects, owner=user, title=self.kwargs['title'])
        return project

    def get_all_project_plugins(self):
        project = self.get_project()
        all_project_plugins = ProjectPlugin.objects.filter(project=project)
        return all_project_plugins

    def get_project_plugin(self):
        all_project_plugins = self.get_all_project_plugins()
        project_plugin = get_object_or_404(all_project_plugins, id=self.kwargs['project_plugin_id'])
        return project_plugin


class CreateProjectPluginView(ProtectedViewMixin, CreateView, ProjectPluginBase):
    form_class = ProjectPluginForm
    template_name = 'edit_plugin.html'

    def get_context_data(self, **kwargs):
        project_plugins = self.get_all_project_plugins()

        context = super(CreateProjectPluginView, self).get_context_data(**kwargs)
        context['action'] = 'Add'
        context['type'] = 'Project Plugin'
        context['project'] = self.kwargs['title']
        context['plugins_'] = project_plugins
        return context

    def form_valid(self, form):
        project = self.get_project()
        data = form.cleaned_data
        kwargs = {
            'title': data['title'],
            'markup': data['markup'],
            'project': project,
        }
        try:
            with transaction.atomic():  # auto-rollback if duplicate
                plugin = ProjectPlugin.objects.create(**kwargs)
                plugin.save()
        except IntegrityError:
            ctx = self.get_context_data(form=form)
            ctx['form_error'] = {
                'title': data['title'],
                'error': 'already exists in this project.'
            }
            return TemplateResponse(self.request, 'edit_plugin.html', context=ctx)

        url_kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['title'],
        }
        ctx = {
            'success_message': 'Project Plugin created!',
            'return_message': 'Project home',
            'return_url': reverse('project_home', kwargs=url_kwargs),
        }
        return TemplateResponse(self.request, 'success.html', context=ctx)


class DeleteProjectPluginView(ProtectedViewMixin, DeleteView, ProjectPluginBase):
    template_name = 'delete_something.html'

    def get_object(self):
        return self.get_project_plugin()

    def get_context_data(self, **kwargs):
        context = super(DeleteProjectPluginView, self).get_context_data(**kwargs)
        context['item'] = self.object.title
        context['project'] = self.kwargs['title']
        return context

    def get_success_url(self):
        kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['title']
        }
        return reverse('project_home', kwargs=kwargs)
