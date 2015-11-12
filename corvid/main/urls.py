from django.conf.urls import url
from .views import ( root_controller, UserHomeView, RegistrationView,
                     CreateProjectView, CreatePageView, UpdatePageView,
                     CreatePostView, UpdatePostView, ProjectDetailView,
                     CreateCategoryView )
from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import logout_then_login as logout_view


urlpatterns = [
    url(r'^$', root_controller, name='root'),
    url(r'^login', login_view, name='login'),
    url(r'^logout', logout_view, name='logout'),
    url(r'^home', UserHomeView.as_view(), name='home'),
    url(r'^register', RegistrationView.as_view(), name='register'),
    url(r'^project/create$', CreateProjectView.as_view(), name='new_project'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/?$',
        ProjectDetailView.as_view(), name='project_home'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/category/new',
        CreateCategoryView.as_view(), name='new_category'),

    # Page URLS
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/page/new',
        CreatePageView.as_view(), name='new_page'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/page/edit/(?P<page_title>[^/]+)',
        UpdatePageView.as_view(), name='edit_page'),

    # Post URLS
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/post/new',
        CreatePostView.as_view(), name='new_post'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/post/edit/(?P<post_title>[^/]+)',
        UpdatePostView.as_view(), name='edit_post'),
]
