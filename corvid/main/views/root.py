from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def root_controller(request):
    if request.method == 'GET':
        return redirect('/home/')
    else:
        return HttpResponse(status=500)
