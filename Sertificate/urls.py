from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/delete_group/(?P<group_id>\d+)/$', views.delete_group),
    url(r'^groups/(?P<group_id>\d+)/issue_cert/(?P<res_id>\d+)/$', views.issue_cert),
    url(r'^groups/(?P<group_id>\d+)/reject_cert/(?P<res_id>\d+)/$', views.reject_cert),
    url(r'^groups/(?P<group_id>\d+)/delete_student/(?P<student_id>\d+)/$', views.delete_student),
    url(r'^add_student/(?P<group_id>\d+)/(?P<student_id>\d+)/$', views.add_student),
    url(r'^search_student/(?P<group_id>\d+)/$', views.search_student),
    url(r'^student_info/(?P<student_id>\d+)/$', views.student_info),
    url(r'^add_task/(?P<student_id>\d+)/(?P<task_id>\d+)/$', views.add_task),
    url(r'^groups/(?P<group_id>\d+)/$', views.groups),
    url(r'^groups/(?P<group_id>\d+)/pay_student/(?P<cert_id>\d+)/$', views.pay_student),
    url(r'^groups/(?P<group_id>\d+)/docs_student/(?P<cert_id>\d+)/$', views.docs_student),
    url(r'^add_group/$', views.add_group),
    url(r'^download/(?P<cert_id>\d+)/$', views.download),
    url(r'^$', views.index),
]

