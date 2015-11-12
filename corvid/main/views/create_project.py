from django.views.generic.edit import CreateView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from main.models import Project, Theme
from .protected_view import ProtectedViewMixin


class CreateProjectView(ProtectedViewMixin, CreateView):
    template_name = 'project_create.html'
    model = Project
    fields = ['title', 'description']
    default_theme = Theme.objects.get(title='default')

    def form_valid(self, form):
        # default theme?
        user = self.request.user
        data = form.cleaned_data
        title = data['title']
        default_theme = Theme.objects.get(title='default')

        kwargs = {
            'title': title,
            'description': data['description'],
            'preview_url': '{0}/{1}'.format(user.username, title),
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
