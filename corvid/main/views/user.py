from django.views.generic import ListView
from .protected_view import ProtectedView
from main.models.project import Project


class UserHomeView(ListView):
    """View that will list all projects belonging to this User"""
    model = Project
    template_name = 'account_home.html'

    def get_queryset(self):
        """Get all projects that belong to this user"""
        return Project.objects.filter(owner=self.request.user)
