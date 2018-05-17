from django.shortcuts import render_to_response
from django.contrib import auth


def index(request):
    args = {'username': auth.get_user(request).username}
    if auth.get_user(request).username:
        args['user_status'] = auth.get_user(request).userprofile.to_rus()
        args['fullname'] = auth.get_user(request).userprofile.fullname
    return render_to_response('index.html', args)


