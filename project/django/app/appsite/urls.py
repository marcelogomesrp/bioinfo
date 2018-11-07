# coding: utf-8
from django.conf.urls.defaults import *


urlpatterns = patterns('appsite.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
)