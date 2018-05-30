from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from Search.forms import SearchForm
from django.core.exceptions import ObjectDoesNotExist
from Sertificate.models import Program, Task, Certificate, Group, User


def search(request):
    user = auth.get_user(request)
    args = {'username': user.username, 'user_status': user.userprofile.to_rus(), 'fullname': user.userprofile.fullname}
    address = 'search.html'
    args.update(csrf(request))
    args['search_form'] = SearchForm()
    if request.POST:
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            return redirect('/search/exec_search/')
        else:
            args['search_form'] = search_form
    return render_to_response(address, args)

