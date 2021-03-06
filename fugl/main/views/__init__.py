from .category import CreateCategoryView, DeleteCategoryView, UpdateCategoryView
from .project import CreateProjectView, DeleteProjectView, CloneProjectView
from .page import CreatePageView, DeletePageView, UpdatePageView
from .post import CreatePostView, DeletePostView, UpdatePostView
from .project_home import ProjectDetailView
from .protected_view import ProtectedViewMixin
from .registration import RegistrationView
from .root import root_controller
from .user import UserHomeView
from .site_generation import SiteGenerationView
from .project_settings import ProjectSettingsView
from .project_plugins import CreateProjectPluginView, UpdateProjectPluginView, DeleteProjectPluginView
from .page_plugins import CreatePagePluginView, UpdatePagePluginView, DeletePagePluginView
