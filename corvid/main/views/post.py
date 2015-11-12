from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from main.models.project import Project
from main.models.post import Post
from main.models.user import User
from .protected_view import ProtectedViewMixin


class CreatePostView(ProtectedViewMixin, CreateView):
    template_name = 'edit_page_post.html'
    model = Post
    fields = ['title', 'category', 'content']

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)

        # This ensures that the user/project exists, and that the visitor is
        # allowed to view it.
        qs = Project.objects.filter(owner=self.request.user)
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        project = get_object_or_404(qs, owner=user, title=self.kwargs['title'])

        context['action'] = 'Add'
        context['type'] = 'Post'
        context['project'] = self.kwargs['title']
        return context

    def form_valid(self, form):
        qs = Project.objects.filter(owner=self.request.user)
        user = get_object_or_404(User.objects, username=self.kwargs['owner'])
        project = get_object_or_404(qs, owner=user, title=self.kwargs['title'])
        data = form.cleaned_data

        # Was getting runtime errors about naive datetime objects.  See:
        # https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
        now = timezone.now()
        kwargs = {
            'title': data['title'],
            'content': data['content'],
            'date_created': now,
            'date_updated': now,
            'project': project,
            'category': data['category'],
        }
        post = Post.objects.create(**kwargs)
        post.save()

        url_kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['title'],
        }
        ctx = {
            'success_message': 'Post created!',
            'return_message': 'Project home',
            'return_url': reverse('project_home', kwargs=url_kwargs),
        }
        return TemplateResponse(self.request, 'success.html', context=ctx)


class UpdatePostView(ProtectedViewMixin, UpdateView):
    template_name = 'edit_page_post.html'
    model = Post
    fields = ['title', 'content']

    def get_object(self):
        project = Project.objects.get(owner=self.request.user, title=self.kwargs['proj_title'])
        post = Post.objects.get(project=project, title=self.kwargs['post_title'])
        return post

    def get_context_data(self, **kwargs):
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['type'] = 'Post'
        context['project'] = self.kwargs['proj_title']
        return context

    def get_success_url(self):
        kwargs = {
            'owner': self.request.user.username,
            'title': self.kwargs['proj_title']
        }
        return reverse('project_home', kwargs=kwargs)
