from django.http import HttpResponse


def get_home(request):
    return HttpResponse('<html><body>Yo.</body></html>')
