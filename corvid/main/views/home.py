from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def get_home(request):
    return HttpResponse('<html><body>Yo.</body></html>')
