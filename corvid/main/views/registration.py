from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse

from main.models import User
from main.forms import RegistrationForm
from .unauthenticated import UnauthenticatedViewMixin


class RegistrationView(UnauthenticatedViewMixin, FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    def form_valid(self, form):

        data = form.cleaned_data
        user = User.objects.create_user(data['username'],
                                        data['email'],
                                        data['password'])
        # due to form validation we know this will be fine
        user.save()
        ctx = {
            'success_message': 'Registration successful',
            'return_message': 'Login page',
            'return_url': reverse('root'),
        }
        return TemplateResponse(self.request, 'success.html', context=ctx)
