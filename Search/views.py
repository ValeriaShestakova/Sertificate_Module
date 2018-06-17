from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from Search.forms import SearchForm
from Sertificate.blockchain import Blockchain
import pickle
import os


blockchain = Blockchain()

if os.path.getsize('data.txt') > 0:
    with open('data.txt', "rb") as f:
        blockchain.chain = pickle.load(f)


def search(request):
    user = auth.get_user(request)
    args = {'username': user.username, 'user_status': user.userprofile.to_rus(), 'fullname': user.userprofile.fullname}
    address = 'search.html'
    # args.update(csrf(request))
    args['search_form'] = SearchForm()
    if request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            search_type = request.GET['search_type']
            search_str = request.GET['search_str']
            if search_type == 'hash':
                data = blockchain.get_data(search_str)
                if len(data) < 1:
                    args['error'] = 'Ничего не найдено'
                else:
                    args['student'] = data['fullname']
            if search_type == 'fullname':
                data = blockchain.get_data_fullname(search_str)
                if len(data) < 1:
                    args['error'] = 'Ничего не найдено'
                else:
                    args['student'] = data['fullname']
        else:
            args['search_form'] = search_form
    return render_to_response(address, args)


