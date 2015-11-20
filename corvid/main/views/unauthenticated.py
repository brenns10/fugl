from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator


def login_unrequired(function):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            ctx = {
                'message': 'You are already logged in.',
                'link_url': '/home/',
                'link_text': 'Go home, you\'re drunk.'
            }
            return TemplateResponse(request, 'error.html', context=ctx)
        else:
            return function(request, *args, **kwargs)
    return inner


class UnauthenticatedViewMixin(object):
    """
    This mixin displays a sad message when you go somewhere that only
    logged-out users should be at.
    """

    @method_decorator(login_unrequired)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
