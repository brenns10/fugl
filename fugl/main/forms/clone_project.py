from django import forms
from django.core.exceptions import ValidationError

from main.models import Project


class CloneProjectForm(forms.ModelForm):
    clone_theme = forms.BooleanField(initial=True, required=False)
    clone_pages = forms.BooleanField(initial=True, required=False)
    clone_posts = forms.BooleanField(initial=True, required=False)
    clone_plugins = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Project
        fields = ['title']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_title(self):
        # Validation - make sure this is the only project with that title by
        # that user.
        if len(Project.objects.filter(owner=self.user,
                                      title=self.cleaned_data['title'])) > 0:
            raise ValidationError('Project with that name already exists.')

        return self.cleaned_data['title']
