from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class ProtectedView(TemplateView):
    """
    Mixin for class views that require an authenticated user.

    Pillaged from https://docs.djangoproject.com/en/1.8/topics/class-based-views/intro/
    """
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)
