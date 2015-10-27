from django.http import HttpResponse
from django.contrib.auth import authenticate

'''
def login_controller(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            # if not ready, redirect to login page
            return HttpResponse('<html>already logged in</html>')
        else:
            # display a page for the user to login
            # TODO: replace with template
            return HttpResponse('<html>login page goes here</html>')
    elif request.method == 'POST':
        # user authentication
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username, password)
        if user.is_active:
            return HttpResponse('<html>login succeeded</html>')
        else:
            return HttpResponse('<html>login failure</html>')
    else:
        return HttpResponse(status=500)
'''
