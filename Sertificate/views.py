from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from .models import Program, Task, Certificate, Group
# select_related prefetch_related only


def index(request):
    args = {'username': auth.get_user(request).username}
    user = auth.get_user(request)
    if user.username:
        args['user_status'] = user.userprofile.to_rus()
        args['fullname'] = user.userprofile.fullname
        if user.userprofile.status == 'student':
            try:
                group = user.userprofile.group
                args['program'] = group.program
            except ObjectDoesNotExist:
                args['error_program'] = 'Текущих курсов не найдено!'
            try:
                cert = Certificate.objects.filter(student=user, status='issued')
                args['certificate'] = cert
            except ObjectDoesNotExist:
                args['error_certificate'] = 'Сертификатов не найдено!'
    return render_to_response('index.html', args)


