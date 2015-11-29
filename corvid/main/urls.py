from django.conf.urls import url
from .views import (root_controller, UserHomeView, RegistrationView,
                    CreateProjectView, CreatePageView, UpdatePageView,
                    CreatePostView, UpdatePostView, ProjectDetailView,
                    CreateCategoryView, SiteGenerationView,
                    ProjectSettingsView)
from .views.unauthenticated import login_unrequired
from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import logout_then_login as logout_view


urlpatterns = [
    url(r'^$', root_controller, name='root'),
    url(r'^login', login_unrequired(login_view), name='login'),
    url(r'^logout', logout_view, name='logout'),
    url(r'^home', UserHomeView.as_view(), name='home'),
    url(r'^register', RegistrationView.as_view(), name='register'),

    # Project URLs
    url(r'^project/create$', CreateProjectView.as_view(), name='new_project'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/settings/?$',
        ProjectSettingsView.as_view(), name='project_settings'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/?$',
        ProjectDetailView.as_view(), name='project_home'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/category/new',
        CreateCategoryView.as_view(), name='new_category'),

    # Page URLS
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/page/new',
        CreatePageView.as_view(), name='new_page'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/page/edit/(?P<page_id>[0-9]+)',
        UpdatePageView.as_view(), name='edit_page'),

    # Post URLS
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/post/new',
        CreatePostView.as_view(), name='new_post'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/post/edit/(?P<post_id>[0-9]+)',
        UpdatePostView.as_view(), name='edit_post'),

    # Site generation
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/generate',
        SiteGenerationView.as_view(), name='site_generation'),
]
