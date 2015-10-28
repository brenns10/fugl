from django.conf.urls import url
from .views.root import root_controller
from .views.user import user_home_controller
from django.contrib.auth.views import login as login_view


urlpatterns = [
    url(r'^$', root_controller),
    url(r'^login', login_view),
    url(r'^home', user_home_controller),
    url(r'^create_account', login_view, name='create_account'),
]
