from django.conf.urls import url
from .views.root import root_controller
from .views.user import UserHomeView
from .views.registration import RegistrationView
from .views.create_project import CreateProjectView
from django.contrib.auth.views import login as login_view


urlpatterns = [
    url(r'^$', root_controller, name='root'),
    url(r'^login', login_view, name='login'),
    url(r'^home', UserHomeView.as_view(), name='home'),
    url(r'^register', RegistrationView.as_view(), name='register'),
    url(r'^new_project', CreateProjectView.as_view(), name='new_project'),
]
