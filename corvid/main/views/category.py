from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django import forms
from main.models import Category, Project, User
from .protected_view import ProtectedViewMixin


class CreateCategoryView(ProtectedViewMixin, CreateView):
    template_name = 'edit_category.html'
    model = Category
    fields = ['title']

    def get_context_data(self, **kwargs):
        qs = Project.objects.filter(owner=self.request.user)
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        project = get_object_or_404(qs, owner=user, title=self.kwargs['title'])
        categories = [c for c in Category.objects.filter(project=project)]

        context = super(CreateCategoryView, self).get_context_data(**kwargs)
        context['action'] = 'Add'
        context['type'] = 'Category'
        context['project'] = self.kwargs['title']
        context['categories_'] = categories
        return context

    def form_valid(self, form):
        qs = Project.objects.filter(owner=self.request.user)
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        project = get_object_or_404(qs, owner=user, title=self.kwargs['title'])
        data = form.cleaned_data
        kwargs = {
            'title': data['title'],
            'project': project
        }
        try:
            category = Category.objects.create(**kwargs)
            category.save()
        except:
            # category already exists; don't care here
            pass
        url_kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['title'],
        }
        ctx = {
            'success_message': 'Category created!',
            'return_message': 'Project home',
            'return_url': reverse('project_home', kwargs=url_kwargs),
        }
        return TemplateResponse(self.request, 'success.html', context=ctx)


class DeleteCategoryView(ProtectedViewMixin, DeleteView):
    template_name = 'delete_something.html'

    def get_object(self):
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        projectqs = Project.objects.filter(owner=self.request.user)
        project = get_object_or_404(projectqs, owner=user, title=self.kwargs['title'])
        categoryqs = Category.objects.filter(project=project)
        category = get_object_or_404(categoryqs, project=project, id=self.kwargs['category_id'])
        return category

    def get_context_data(self, **kwargs):
        context = super(DeleteCategoryView, self).get_context_data(**kwargs)
        context['item'] = self.object.title
        context['project'] = self.kwargs['title']
        return context

    def get_success_url(self):
        kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['title']
        }
        return reverse('project_home', kwargs=kwargs)
