from django.shortcuts import render_to_response, redirect
from django.http.response import Http404
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from .models import Program, Task, Certificate, Group, User
from userprofile.models import UserProfile
from django.template.context_processors import csrf
from loginsys.forms import SignUpForm
from Sertificate.forms import GroupForm
import random
# select_related prefetch_related only


def index(request):
    user = auth.get_user(request)
    args = {'username': user.username, 'stud': user}
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
                    args['group'] = group
                    args['teachers'] = group.teacher.all()
                    cert = Certificate.objects.get(student=user, program=group.program)
                    args['cert'] = cert
                    if cert.status == 'issued' or cert.status == 'not_issued':
                        args['error_program'] = 'Текущих курсов не найдено!'
                        args['group'] = ''
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
            args['groups'] = groups
            if ~groups.exists():
                args['error_groups'] = 'Групп не найдено'
            students_prof = UserProfile.objects.filter(group_for_stud__in=groups)
            students = User.objects.filter(userprofile__in=students_prof)
            cert = Certificate.objects.filter(student__in=students, status='required')
            args['cert'] = cert
            if ~cert.exists():
                args['error_request'] = 'Запросов не найдено'
        if user.userprofile.status == 'secretary':
            address = 'index_secretary.html'
            groups = Group.objects.all()
            args['groups'] = groups
            if ~groups.exists():
                args['error_groups'] = 'Групп не найдено'
    return render_to_response(address, args)


def issue_cert(request, cert_id, group_id=0):
    try:
        certificate = Certificate.objects.get(id=cert_id)
        certificate.status = 'issued'
        certificate.save()
        address = "/"
        if int(group_id) > 0:
            address = '/groups/%s/' % group_id
    except ObjectDoesNotExist:
        raise Http404
    return redirect(address)


def reject_cert(request, cert_id, group_id=0):
    try:
        certificate = Certificate.objects.get(id=cert_id)
        certificate.status = 'not_issued'
        certificate.save()
        address = "/"
        if int(group_id) > 0:
            address = '/groups/%s/' % group_id
    except ObjectDoesNotExist:
        raise Http404
    return redirect(address)


def require_cert(request, cert_id):
    try:
        certificate = Certificate.objects.get(id=cert_id)
        certificate.status = 'required'
        certificate.save()
        address = "/"
    except ObjectDoesNotExist:
        raise Http404
    return redirect(address)


def groups(request, group_id):
    user = auth.get_user(request)
    args = {'username': user.username, 'status': user.userprofile.status}
    address = 'groups.html'
    args['user_status'] = user.userprofile.to_rus()
    args['fullname'] = user.userprofile.fullname
    group = Group.objects.get(id=group_id)
    args['group'] = group
    students_prof = UserProfile.objects.filter(group_for_stud=group)
    students = User.objects.filter(userprofile__in=students_prof)
    cert = Certificate.objects.filter(student__in=students)
    args['cert'] = cert
    if ~cert.exists():
        args['error_students'] = 'Студентов не найдено'
    return render_to_response(address, args)


def delete_student(request, student_id, group_id=0):
    try:
        student = User.objects.get(id=student_id)
        group = Group.objects.get(id=group_id)
        student.userprofile.group_for_stud = None
        student.userprofile.task.clear()
        student.save()
        address = "/"
        cert = Certificate.objects.get(student=student, program=group.program)
        if cert.status != 'issued':
            cert.delete()
        if int(group_id) > 0:
            address = '/groups/%s/' % group_id
    except ObjectDoesNotExist:
        raise Http404
    return redirect(address)


def add_student(request, group_id, student_id=0):
    user = auth.get_user(request)
    args = {'username': user.username, 'user_status': user.userprofile.to_rus(), 'fullname': user.userprofile.fullname,
            'group_id': group_id}
    address = 'add_student.html'
    group = Group.objects.get(id=group_id)
    if int(student_id) > 1:
        student = User.objects.get(id=student_id)
        gr = student.userprofile.group_for_stud
        if gr is None:
            student.userprofile.group_for_stud = group
            student.userprofile.task.clear()
            student.save()
            cert = Certificate()
            cert.certificate_number = cert_number()
            cert.status = 'not_required'
            cert.program = group.program
            cert.student = student
            cert.save()
            address = '/groups/%s/' % group_id
            args['error'] = ''
            return redirect(address)
        else:
            args['error'] = 'Ошибка! Пользователь %s уже состоит в группе %s' % (student.userprofile.fullname, gr.group_number)
    args.update(csrf(request))
    args['form'] = SignUpForm()
    if int(student_id) == 1:
        if request.POST:
            newuser_form = SignUpForm(request.POST)
            if newuser_form.is_valid():
                user = newuser_form.save()
                user.refresh_from_db()
                user.userprofile.fullname = newuser_form.cleaned_data.get('fullname')
                user.userprofile.status = 'student'
                user.userprofile.group_for_stud = group
                user.userprofile.task.clear()
                user.save()
                cert = Certificate()
                cert.certificate_number = cert_number()
                cert.status = 'not_required'
                cert.program = group.program
                cert.student = user
                cert.save()
                address = '/groups/%s/' % group_id
                return redirect(address)
            else:
                args['form'] = newuser_form
                args['registration_error'] = 'Ошибка регистрации'
    return render_to_response(address, args)


def cert_number():
    cert_number = random.randrange(100000, 1000000, 1)
    return cert_number


def search_student(request, group_id):
    user = auth.get_user(request)
    args = {'username': user.username, 'user_status': user.userprofile.to_rus(), 'fullname': user.userprofile.fullname,
            'group_id': group_id}
    address = 'add_student.html'
    try:
        fullname = request.GET['fullname']
        student = UserProfile.objects.get(fullname=fullname).user
        error = ""
        args['student'] = student
    except ObjectDoesNotExist:
        error = "Ошибка! Ничего не найдено!"
    args['error'] = error
    return render_to_response(address, args)


def add_group(request):
    user = auth.get_user(request)
    args = {'username': user.username, 'user_status': user.userprofile.to_rus(), 'fullname': user.userprofile.fullname}
    address = 'add_group.html'
    args.update(csrf(request))
    args['group_form'] = GroupForm()
    if request.POST:
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            return redirect('/')
        else:
            args['group_form'] = group_form
            args['error'] = 'Ошибка!'
    return render_to_response(address, args)


def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    students = UserProfile.objects.filter(group_for_stud=group)
    for st in students:
        st.group_for_stud = None
        user = User.objects.get(userprofile=st)
        st.userprofile.task.clear()
        try:
            cert = Certificate.objects.get(student=user, program=group.program)
            if cert.status != 'issued':
                cert.delete()
        except ObjectDoesNotExist:
            error = 'Сертификатов нет'
    group.delete()
    return redirect('/')


def student_info(request, student_id):
    user = auth.get_user(request)
    args = {'username': user.username, 'user_status': user.userprofile.to_rus(), 'fullname': user.userprofile.fullname}
    address = 'student_info.html'
    student = User.objects.get(id=student_id)
    cert = Certificate.objects.get(student=student, program=student.userprofile.group_for_stud.program)
    t = student.userprofile.task.all()
    task = Task.objects.exclude(id__in=t)
    tasks = Task.objects.filter(id__in=task, program=student.userprofile.group_for_stud.program)
    args['student'] = student
    args['cert'] = cert
    args['tasks'] = tasks
    return render_to_response(address, args)


def add_task(request, student_id, task_id):
    address = '/student_info/%s/' % student_id
    student = User.objects.get(id=student_id)
    task = Task.objects.get(id=task_id)
    student.userprofile.task.add(task)
    student.save()
    return redirect(address)


def search(request):
    user = auth.get_user(request)
    args = {'username': user.username, 'user_status': user.userprofile.to_rus(), 'fullname': user.userprofile.fullname}
    address = 'search.html'
    return render_to_response(address, args)


