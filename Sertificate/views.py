from django.shortcuts import render_to_response, redirect
from django.http.response import Http404
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from .models import Result, Task, Certificate, Group, User
from userprofile.models import UserProfile
from django.template.context_processors import csrf
from Sertificate.forms import GroupForm
from django.http import HttpResponse
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
                    result = Result.objects.get(student=user, certificate=cert)
                    args['cert'] = cert
                    args['result'] = result
                    if cert.status != 'create':
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


def pay_student(request, group_id, cert_id):
    try:
        cert = Certificate.objects.get(id=cert_id)
        cert.pay = True
        cert.save()
        change_status(cert_id)
        address = '/groups/%s/' % group_id
    except ObjectDoesNotExist:
        raise Http404
    return redirect(address)


def docs_student(request, group_id, cert_id):
    try:
        cert = Certificate.objects.get(id=cert_id)
        cert.docs = True
        cert.save()
        change_status(cert_id)
        address = '/groups/%s/' % group_id
    except ObjectDoesNotExist:
        raise Http404
    return redirect(address)


def issue_cert(request, res_id, group_id=0):
    try:
        res = Result.objects.get(id=res_id)
        res.approved = True
        res.save()
        change_status(res.certificate.id)
        address = "/"
        if int(group_id) > 0:
            address = '/groups/%s/' % group_id
    except ObjectDoesNotExist:
        raise Http404
    return redirect(address)


def reject_cert(request, res_id, group_id=0):
    try:
        res = Result.objects.get(id=res_id)
        res.certificate.change = False
        res.certificate.status = 'reject'
        res.certificate.save()
        res.save()
        address = "/"
        if int(group_id) > 0:
            address = '/groups/%s/' % group_id
    except ObjectDoesNotExist:
        raise Http404
    return redirect(address)


def groups(request, group_id):
    user = auth.get_user(request)
    args = {'username': user.username, 'status': user.userprofile.status, 'user_status': user.userprofile.to_rus(),
            'fullname': user.userprofile.fullname}
    group = Group.objects.get(id=group_id)
    args['group'] = group
    students_prof = UserProfile.objects.filter(group_for_stud=group)
    students = User.objects.filter(userprofile__in=students_prof)
    if user.userprofile.status == 'teacher':
        address = 'group_for_teacher.html'
        result = Result.objects.filter(student__in=students)
        args['result'] = result
        if ~result.exists():
            args['error_students'] = 'Студентов не найдено'
    if user.userprofile.status == 'secretary':
        address = 'group_for_secretary.html'
        cert = Certificate.objects.filter(student__in=students)
        args['cert'] = cert
        if ~cert.exists():
            args['error_students'] = 'Студентов не найдено'
    return render_to_response(address, args)


def delete_student(request, student_id, group_id=0):
    try:
        address = "/"
        student = User.objects.get(id=student_id)
        group = Group.objects.get(id=group_id)
        student.userprofile.group_for_stud = None
        student.save()
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
            student.save()
            cert = Certificate()
            cert.certificate_number = cert_number()
            cert.program = group.program
            cert.student = student
            cert.save()
            res = Result()
            res.student = student
            res.certificate = cert
            res.save()
            address = '/groups/%s/' % group_id
            args['error'] = ''
            return redirect(address)
        else:
            args['error'] = 'Ошибка! Пользователь %s уже состоит в группе %s' % (student.userprofile.fullname, gr.group_number)
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
    res = Result.objects.get(student=student, certificate=cert)
    t = res.task.all()
    task = Task.objects.exclude(id__in=t)
    tasks = Task.objects.filter(id__in=task, program=cert.program)
    args['student'] = student
    args['res'] = res
    args['tasks'] = tasks
    return render_to_response(address, args)


def add_task(request, student_id, task_id):
    address = '/student_info/%s/' % student_id
    student = User.objects.get(id=student_id)
    task = Task.objects.get(id=task_id)
    cert = Certificate.objects.get(student=student, program=task.program)
    res = Result.objects.get(student=student, certificate=cert)
    res.task.add(task)
    student.save()
    return redirect(address)


def backup(request):
    user = auth.get_user(request)
    args = {'username': user.username, 'user_status': user.userprofile.to_rus(), 'fullname': user.userprofile.fullname}
    address = '/'
    # memcon = apsw.Connection(":memory:")
    # # Copy into memory
    # connection = "C:/Users/Valeria/PycharmProjects/SertificateModule/venv/Scripts/SertificateModule/db.sqlite3"
    # with memcon.backup("main", connection, "main") as backup:
    #     backup.step()  # copy whole database in one go
    #
    # # There will be no disk accesses for this query
    # for row in memcon.cursor().execute("select * from s"):
    #     pass
    return redirect(address)


def show_pdf(request):
    with open('static/file.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=file.pdf'
        return response
    pdf.closed
    return response


def change_status(cert_id):
    cert = Certificate.objects.get(id=cert_id)
    if cert.docs and cert.pay and cert.change and cert.result.approved:
        cert.status = 'issued'
        cert.change = False
        cert.save()
    return cert

