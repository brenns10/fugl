from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django import forms
from pagedown.widgets import PagedownWidget

from main.models import Project, Page, User
from .protected_view import ProtectedViewMixin


class PageForm(forms.ModelForm):

    content = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Page
        fields = ['title', 'content']


class CreatePageView(ProtectedViewMixin, CreateView):
    form_class = PageForm
    template_name = 'edit_page_post.html'

    def get_context_data(self, **kwargs):
        context = super(CreatePageView, self).get_context_data(**kwargs)

        # Verify that the request is coming into a real user and project:
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        qs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(qs, owner=user, title=self.kwargs['title'])

        context['action'] = 'Add'
        context['type'] = 'Page'
        context['project'] = self.kwargs['title']
        return context

    def form_valid(self, form):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        qs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(qs, owner=user, title=self.kwargs['title'])
        data = form.cleaned_data
        kwargs = {
            'title': data['title'],
            'content': data['content'],
            'project': project
        }
        page = Page.objects.create(**kwargs)
        page.save()
        url_kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['title'],
        }
        ctx = {
            'success_message': 'Page created!',
            'return_message': 'Project home',
            'return_url': reverse('project_home', kwargs=url_kwargs),
        }
        return TemplateResponse(self.request, 'success.html', context=ctx)


class UpdatePageView(ProtectedViewMixin, UpdateView):
    form_class = PageForm
    template_name = 'edit_page_post.html'

    def get_object(self):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        projectqs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(projectqs, owner=user, title=self.kwargs['proj_title'])
        page = get_object_or_404(Page.objects, project=project, title=self.kwargs['page_title'])
        return page

    def get_context_data(self, **kwargs):
        context = super(UpdatePageView, self).get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['type'] = 'Page'
        context['project'] = self.kwargs['proj_title']
        return context

    def get_success_url(self):
        kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['proj_title']
        }
        return reverse('project_home', kwargs=kwargs)
