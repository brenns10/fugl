from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from main.models.user import User
from main.forms.registration import RegistrationForm


class RegistrationView(FormView):
    template_name = 'form.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(data['username'],
                                        data['email'],
                                        data['password'])
        if user is None:
            raise ValidationError('Unable to create user')
        else:
            user.save()
            ctx = {
                'success_message': 'Registration successful',
                'return_message': 'Login page',
                'return_url': reverse('root'),
            }
            return TemplateResponse(self.request, 'success.html', context=ctx)
