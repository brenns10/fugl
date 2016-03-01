from django.conf.urls import url
from .views import (root_controller, UserHomeView, RegistrationView,
                    CreateProjectView, DeleteProjectView,
                    CreatePageView, UpdatePageView, DeletePageView,
                    CreatePostView, UpdatePostView, DeletePostView,
                    ProjectDetailView, SiteGenerationView,
                    CreateCategoryView, UpdateCategoryView, DeleteCategoryView,
                    CreateProjectPluginView, UpdateProjectPluginView, DeleteProjectPluginView,
                    CreatePagePluginView, UpdatePagePluginView, DeletePagePluginView,
                    ProjectSettingsView, CloneProjectView)
from .views.unauthenticated import login_unrequired
from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import logout_then_login as logout_view


urlpatterns = [
    url(r'^$', root_controller, name='root'),
    url(r'^login\.php$', login_unrequired(login_view), name='login'),
    url(r'^logout\.php$', logout_view, name='logout'),
    url(r'^home\.php$', UserHomeView.as_view(), name='home'),
    url(r'^register\.php$', RegistrationView.as_view(), name='register'),

    # Project URLs
    url(r'^project/create\.php$', CreateProjectView.as_view(), name='new_project'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/delete\.php$',
        DeleteProjectView.as_view(), name='delete_project'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/settings\.php$',
        ProjectSettingsView.as_view(), name='project_settings'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)\.php$',
        ProjectDetailView.as_view(), name='project_home'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/clone\.php?$',
        CloneProjectView.as_view(), name='clone_project'),

    # Category URLs
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/category/new\.php$',
        CreateCategoryView.as_view(), name='new_category'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/category/delete/(?P<category_id>[0-9]+)\.php$',
        DeleteCategoryView.as_view(), name='delete_category'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/category/edit/(?P<category_id>[0-9]+)\.php$',
        UpdateCategoryView.as_view(), name='edit_category'),

    # Page URLS
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/page/new\.php$',
        CreatePageView.as_view(), name='new_page'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/page/edit/(?P<page_id>[0-9]+)\.php$',
        UpdatePageView.as_view(), name='edit_page'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/page/delete/(?P<page_id>[0-9]+)\.php$',
        DeletePageView.as_view(), name='delete_page'),

    # Post URLS
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/post/new\.php$',
        CreatePostView.as_view(), name='new_post'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/post/edit/(?P<post_id>[0-9]+)\.php$',
        UpdatePostView.as_view(), name='edit_post'),
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/post/delete/(?P<post_id>[0-9]+)\.php$',
        DeletePostView.as_view(), name='delete_post'),

    # Plugin URLs
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/project_plugin/new\.php$',
        CreateProjectPluginView.as_view(), name='new_project_plugin'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/project_plugin'
        '/edit/(?P<project_plugin_id>[0-9]+)\.php$',
        UpdateProjectPluginView.as_view(), name='edit_project_plugin'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/project_plugin'
        '/delete/(?P<project_plugin_id>[0-9]+)\.php$',
        DeleteProjectPluginView.as_view(), name='delete_project_plugin'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/page_plugin/new\.php$',
        CreatePagePluginView.as_view(), name='new_page_plugin'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/page_plugin'
        '/edit/(?P<page_plugin_id>[0-9]+)\.php$',
        UpdatePagePluginView.as_view(), name='edit_page_plugin'),
    url(r'^project/(?P<owner>[^/]+)/(?P<title>[^/]+)/page_plugin'
        '/delete/(?P<page_plugin_id>[0-9]+)\.php$',
        DeletePagePluginView.as_view(), name='delete_page_plugin'),

    # Site generation
    url(r'^project/(?P<owner>[^/]+)/(?P<proj_title>[^/]+)/generate\.php$',
        SiteGenerationView.as_view(), name='site_generation'),
]
