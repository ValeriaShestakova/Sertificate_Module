from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from loginsys.forms import SignUpForm


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = SignUpForm()
    if request.POST:
        newuser_form = SignUpForm(request.POST)
        if newuser_form.is_valid():
            user = newuser_form.save()
            user.refresh_from_db()
            user.userprofile.fullname = newuser_form.cleaned_data.get('fullname')
            user.userprofile.status = 'student'
            user.save()
            raw_password = newuser_form.cleaned_data.get('password1')
            user = auth.authenticate(username=user.username, password=raw_password)
            auth.login(request, user)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)
