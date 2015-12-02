from django import forms
from django.core.exceptions import ValidationError
from main.models import Project


class CreateProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Capture the user!
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['title', 'description']

    def clean_title(self):
        # Validation - make sure this is the only project with that title by
        # that user.
        if len(Project.objects.filter(owner=self.user,
                                      title=self.cleaned_data['title'])) > 0:
            raise ValidationError('Project with that name already exists.')

        # More validation - make sure this title has no forward slashes:
        if '/' in self.cleaned_data['title']:
            raise ValidationError('Project title may not contain forward slash'
                                  ' ("/").')

        return self.cleaned_data['title']
