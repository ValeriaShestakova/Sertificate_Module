from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^exec_search/$', views.search),
    ]
