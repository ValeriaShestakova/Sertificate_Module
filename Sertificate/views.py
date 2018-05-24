from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from .models import Program, Task, Certificate, Group, User
from userprofile.models import UserProfile
# select_related prefetch_related only


def index(request):
    args = {'username': auth.get_user(request).username}
    user = auth.get_user(request)
    address = 'main.html'
    if user.username:
        args['user_status'] = user.userprofile.to_rus()
        args['fullname'] = user.userprofile.fullname
        if user.userprofile.status == 'student':
            address = 'index_student.html'
            try:
                group = user.userprofile.group_for_stud
                if group is None:
                    args['error_program'] = 'Текущих курсов не найдено!'
                else:
                    args['program'] = group.program
            except ObjectDoesNotExist:
                args['error_program'] = 'Текущих курсов не найдено!'
            try:
                cert = Certificate.objects.filter(student=user, status='issued')
                args['certificate'] = cert
            except ObjectDoesNotExist:
                args['error_certificate'] = 'Сертификатов не найдено!'
        if user.userprofile.status == 'teacher':
            address = 'index_teacher.html'
            groups = Group.objects.filter(teacher=user)
            students_prof = UserProfile.objects.filter(group_for_stud__in=groups)
            students = User.objects.filter(userprofile__in=students_prof)
            cert = Certificate.objects.filter(student__in=students, status='required')
            req = []
            for c in cert:
                str = c.student.userprofile.fullname + ', Группа ' + Group.objects.get(
                    program=c.program).group_number
                req.append(str)
            args['req'] = req
            if ~cert.exists():
                args['error_request'] = 'Запросов не найдено'
    return render_to_response(address, args)


