from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from main.models.project import Project
from main.models.page import Page
from .protected_view import ProtectedViewMixin


class CreatePageView(ProtectedViewMixin, CreateView):
    template_name = 'edit_page_post.html'
    model = Page
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super(CreatePageView, self).get_context_data(**kwargs)
        context['action'] = 'Add'
        context['type'] = 'Page'
        context['project'] = self.kwargs['title']
        return context

    def form_valid(self, form):
        project = Project.objects.get(owner=self.request.user, title=self.kwargs['title'])
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
    template_name = 'edit_page_post.html'
    model = Page
    fields = ['title', 'content']

    def get_object(self):
        project = Project.objects.get(owner=self.request.user, title=self.kwargs['proj_title'])
        page = Page.objects.get(project=project, title=self.kwargs['page_title'])
        return page

    def get_context_data(self, **kwargs):
        context = super(UpdatePageView, self).get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['type'] = 'Page'
        return context

    def get_success_url(self):
        kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['proj_title']
        }
        return reverse('project_home', kwargs=kwargs)
