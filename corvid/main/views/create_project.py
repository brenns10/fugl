from django.views.generic.edit import CreateView
from django.http import HttpResponse
from main.models.project import Project
from main.models.theme import Theme


class CreateProjectView(CreateView):
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
            'preview_url': '/'.join([user.username, title]),
            'owner': user,
            'theme': default_theme,
        }
        proj = Project.objects.create(**kwargs)
        proj.save()
        return HttpResponse('<html>Project created: {0}</html>'.format(title))
