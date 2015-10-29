from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProtectedViewMixin(object):
    """
    Mixin for class views that require an authenticated user.

    Pillaged from https://docs.djangoproject.com/en/1.8/topics/class-based-views/intro/
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)
