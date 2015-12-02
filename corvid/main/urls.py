from django.conf.urls import url
from .views import (root_controller, UserHomeView, RegistrationView,
                    CreateProjectView, DeleteProjectView,
                    CreatePageView, UpdatePageView, DeletePageView,
                    CreatePostView, UpdatePostView, DeletePostView,
                    ProjectDetailView, SiteGenerationView,
                    CreateCategoryView, UpdateCategoryView, DeleteCategoryView,
                    CreateProjectPluginView, UpdateProjectPluginView, DeleteProjectPluginView,
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
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/delete/?$',
        DeleteProjectView.as_view(), name='delete_project'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/settings/?$',
        ProjectSettingsView.as_view(), name='project_settings'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/?$',
        ProjectDetailView.as_view(), name='project_home'),

    # Category URLs
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/category/new',
        CreateCategoryView.as_view(), name='new_category'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/category/delete/(?P<category_id>[0-9]+)/?',
        DeleteCategoryView.as_view(), name='delete_category'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/category/edit/(?P<category_id>[0-9]+)/?',
        UpdateCategoryView.as_view(), name='edit_category'),

    # Page URLS
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/page/new',
        CreatePageView.as_view(), name='new_page'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/page/edit/(?P<page_id>[0-9]+)',
        UpdatePageView.as_view(), name='edit_page'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/page/delete/(?P<page_id>[0-9]+)/?',
        DeletePageView.as_view(), name='delete_page'),

    # Post URLS
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/post/new',
        CreatePostView.as_view(), name='new_post'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/post/edit/(?P<post_id>[0-9]+)',
        UpdatePostView.as_view(), name='edit_post'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/post/delete/(?P<post_id>[0-9]+)',
        DeletePostView.as_view(), name='delete_post'),

    # Plugin URLs
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/project_plugin/new',
        CreateProjectPluginView.as_view(), name='new_project_plugin'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/project_plugin'
        '/edit/(?P<project_plugin_id>[0-9]+)/?',
        UpdateProjectPluginView.as_view(), name='edit_project_plugin'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/project_plugin'
        '/delete/(?P<project_plugin_id>[0-9]+)/?',
        DeleteProjectPluginView.as_view(), name='delete_project_plugin'),


    # Site generation
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/generate',
        SiteGenerationView.as_view(), name='site_generation'),
]
