from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
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
        return HttpResponse('<html>Page saved: {0}/{1}</html>'.format(project.title, data['title']))


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
