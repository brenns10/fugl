from django.conf.urls import url
from .views.root import root_controller
from .views.user import user_home_controller
from .views.registration import RegistrationView
from .forms.login import LoginForm
from django.contrib.auth.views import login as login_view


urlpatterns = [
    url(r'^$', root_controller),
    url(r'^login', login_view),
    url(r'^home', user_home_controller),
    url(r'^register', RegistrationView.as_view()),
]
