# coding: utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^classes/(?P<class_id>\d+)/add/$', views.add_class, 
        name='calendar_add_class'),
    url(r'^classes/(?P<classenrollment_id>\d+)/$', views.list_classes, 
        name='calendar_list_classes'),
    url(r'^instr/classes/(?P<class_id>\d+)/$', views.instructor_list_classes, 
        name='calendar_instructor_list_classes'),
)