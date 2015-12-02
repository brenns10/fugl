from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from main.models import Project, Theme, User
from main.forms import CreateProjectForm, CloneProjectForm
from .protected_view import ProtectedViewMixin


class CreateProjectView(ProtectedViewMixin, FormView):
    form_class = CreateProjectForm
    template_name = 'project_create.html'
    default_theme = Theme.objects.get(title='default')

    def get_form_kwargs(self):
        """
        Put the request user into the form constructor kwargs so it can use it.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        # default theme?
        user = self.request.user
        data = form.cleaned_data
        title = data['title']
        default_theme = Theme.objects.get(title='default')

        kwargs = {
            'title': title,
            'description': data['description'],
            'preview_url': '',
            'owner': user,
            'theme': default_theme,
        }
        proj = Project.objects.create(**kwargs)
        proj.save()
        ctx = {
            'success_message': 'Project created!',
            'return_message': 'Project home',
            'return_url': reverse('project_home', kwargs={'owner': user.username, 'title': title}),
        }
        return TemplateResponse(self.request, 'success.html', context=ctx)


class CloneProjectView(ProtectedViewMixin, FormView):
    form_class = CloneProjectForm
    template_name = 'project_clone.html'
    default_theme = Theme.objects.get(title='default')

    def get_form_kwargs(self):
        """
        Put the request user into the form constructor kwargs so it can use it.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # These just ensure that we will 404 if:
        # - the user doesn't exist
        # - the project doesn't exist
        # - the project isn't owned by the user
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        projectqs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(projectqs, owner=user,
                                    title=self.kwargs['title'])

        context['project'] = self.kwargs['title']
        return context

    def form_valid(self, form):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        projectqs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(projectqs, owner=user,
                                    title=self.kwargs['title'])
        data = form.cleaned_data
        project.clone(data['title'], data['clone_theme'], data['clone_pages'],
                      data['clone_posts'], data['clone_plugins'])
        ctx = {
            'success_message': 'Project cloned!',
            'return_message': 'Cloned project home',
            'return_url': reverse('project_home',
                                  kwargs={'owner': user.username,
                                          'title': data['title']}),
        }
        return TemplateResponse(self.request, 'success.html', context=ctx)


class DeleteProjectView(ProtectedViewMixin, DeleteView):
    template_name = 'delete_something.html'

    def get_object(self):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        projectqs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(projectqs, owner=user, title=self.kwargs['title'])
        return project

    def get_context_data(self, **kwargs):
        context = super(DeleteProjectView, self).get_context_data(**kwargs)
        context['item'] = None
        context['project'] = self.object.title
        return context

    def get_success_url(self):
        return reverse('home')
