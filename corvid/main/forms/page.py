from django import forms

from pagedown.widgets import PagedownWidget

from ..models import Page


class PageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Order is important here: project must be removed from kwargs or super
        # constructor fails.  Querysets must be modified after super
        # constructor finishes, otherwise the self.fields dict is not yet
        # initialized.
        project = kwargs.pop('__project')
        super(PageForm, self).__init__(*args, **kwargs)
        plugins = project.pageplugin_set.all()
        self.fields['post_plugins'].queryset = plugins
        self.fields['post_plugins'].required = False
        self.fields['post_plugins'].label = 'Page plugins'

    class Meta:
        model = Page
        fields = ['title', 'post_plugins', 'content']
        widgets = {
            'content': PagedownWidget(),
        }
        help_texts = {
            'post_plugins': 'Hold "Control" while clicking to select multiple.'
        }
