from django.http import HttpResponse


def user_home_controller(request):
    return HttpResponse('<html>User home goes here.</html>')
