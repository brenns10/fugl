from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
from django.http import HttpResponse
from main.models.user import User
from main.forms.register import RegistrationForm


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
            return HttpResponse('<html>registration successful</html>')
