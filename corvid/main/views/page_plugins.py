from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django import forms
from main.models import Project, User, PagePlugin
from .protected_view import ProtectedViewMixin


class PagePluginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # User may not need these fields: let the submit it blank if need-be
        self.fields['head_markup'].required = False
        self.fields['body_markup'].required = False

    class Meta:
        model = PagePlugin
        fields = ['title', 'head_markup', 'body_markup']


class PagePluginBase(object):
    def get_project(self):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        user_projects = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(user_projects, owner=user, title=self.kwargs['title'])
        return project

    def get_all_page_plugins(self):
        project = self.get_project()
        return project.pageplugin_set.all()

    def get_page_plugin(self):
        all_page_plugins = self.get_all_page_plugins()
        page_plugin = get_object_or_404(all_page_plugins, id=self.kwargs['page_plugin_id'])
        return page_plugin


class CreatePagePluginView(ProtectedViewMixin, CreateView, PagePluginBase):
    form_class = PagePluginForm
    template_name = 'edit_plugin.html'

    def get_context_data(self, **kwargs):
        page_plugins = self.get_all_page_plugins()

        context = super(CreatePagePluginView, self).get_context_data(**kwargs)
        context['action'] = 'Add'
        context['type'] = 'Page Plugin'
        context['project'] = self.kwargs['title']
        context['plugins_'] = page_plugins
        return context

    def form_valid(self, form):
        project = self.get_project()
        data = form.cleaned_data
        kwargs = {
            'title': data['title'],
            'head_markup': data['head_markup'],
            'body_markup': data['body_markup'],
            'project': project,
        }
        try:
            with transaction.atomic():  # auto-rollback if duplicate
                plugin = PagePlugin.objects.create(**kwargs)
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
            'success_message': 'Page Plugin created!',
            'return_message': 'Project home',
            'return_url': reverse('project_home', kwargs=url_kwargs),
        }
        return TemplateResponse(self.request, 'success.html', context=ctx)


class DeletePagePluginView(ProtectedViewMixin, DeleteView, PagePluginBase):
    template_name = 'delete_something.html'

    def get_object(self):
        return self.get_page_plugin()

    def get_context_data(self, **kwargs):
        context = super(DeletePagePluginView, self).get_context_data(**kwargs)
        context['item'] = self.object.title
        context['project'] = self.kwargs['title']
        return context

    def get_success_url(self):
        kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['title']
        }
        return reverse('project_home', kwargs=kwargs)


class UpdatePagePluginView(ProtectedViewMixin, UpdateView, PagePluginBase):
    form_class = PagePluginForm
    template_name = 'edit_plugin.html'

    def get_object(self):
        return self.get_page_plugin()

    def get_context_data(self, **kwargs):
        page_plugins = self.get_all_page_plugins()

        context = super(UpdatePagePluginView, self).get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['type'] = 'Page Plugin'
        context['project'] = self.kwargs['title']
        context['plugins_'] = page_plugins
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():  # Auto-rollback on error
                return super(UpdatePagePluginView, self).form_valid(form)
        except IntegrityError:
            ctx = self.get_context_data(form=form)
            ctx['form_error'] = {
                'title': form.cleaned_data['title'],
                'error': ' already exists in this project '
            }
            return TemplateResponse(self.request, 'edit_plugin.html', context=ctx)

    def get_success_url(self):
        kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['title']
        }
        return reverse('project_home', kwargs=kwargs)
