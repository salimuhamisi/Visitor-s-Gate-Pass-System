from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_usernames=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            username = request.user.username
            if username in allowed_usernames:
                return view_func(request, *args, **kwargs)  
            else:
                return HttpResponse('You are not allowed to access this page')

        return wrapper_func
    return decorator
