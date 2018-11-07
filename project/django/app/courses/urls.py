# coding: utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^list/(?P<institution_id>\d+)/$', views.list_classes_by_institution, name='list_classes_by_institution'),
    url(r'^view/(?P<class_id>\d+)/$', views.class_detail, name='class_detail'),
    url(r'^(?P<code>[\w-]+)/$', views.class_permalink, name='class_permalink'),
)
