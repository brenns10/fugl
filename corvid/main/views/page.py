from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django import forms
from pagedown.widgets import PagedownWidget

from main.models import Project, Page, User, PagePlugin
from .protected_view import ProtectedViewMixin


class PageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        '''
        DON'T CHANGE THE ORDER LEST YOU WISH TO BREAK CATEGORIES
        '''
        project = kwargs.pop('__project')
        super(PageForm, self).__init__(*args, **kwargs)
        plugins = project.pageplugin_set.all()
        self.fields['post_plugins'].queryset = plugins

    content = forms.CharField(widget=PagedownWidget())
    # Added Empty queryset to satisfy Field's constructor until PostForm's is called.
    post_plugins = forms.ModelMultipleChoiceField(queryset=PagePlugin.objects.none(),
                                                  required=False)
    class Meta:
        model = Page
        fields = ['title', 'content', 'post_plugins']


class PageBase:
    def get_page_object(self):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        projectqs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(projectqs, owner=user, title=self.kwargs['proj_title'])
        page = get_object_or_404(Page.objects, project=project, id=self.kwargs['page_id'])
        return page


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

    def get_form_kwargs(self):
        initial = super().get_form_kwargs()
        qs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(qs, owner=self.request.user, title=self.kwargs['title'])
        initial['__project'] = project
        return initial

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
        page.post_plugins.add(*data['post_plugins'])
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


class DeletePageView(ProtectedViewMixin, DeleteView, PageBase):
    form_class = PageForm
    template_name = 'delete_something.html'

    def get_object(self):
        return self.get_page_object()

    def get_context_data(self, **kwargs):
        context = super(DeletePageView, self).get_context_data(**kwargs)
        context['project'] = self.kwargs['proj_title']
        context['item'] = self.object.title
        return context

    def get_success_url(self):
        kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['proj_title']
        }
        return reverse('project_home', kwargs=kwargs)


class UpdatePageView(ProtectedViewMixin, UpdateView, PageBase):
    form_class = PageForm
    template_name = 'edit_page_post.html'

    def get_object(self):
        return self.get_page_object()

    def get_form_kwargs(self):
        initial = super().get_form_kwargs()
        qs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(qs, owner=self.request.user,
                                    title=self.kwargs['proj_title'])
        initial['__project'] = project
        return initial

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
