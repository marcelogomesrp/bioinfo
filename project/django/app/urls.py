# coding: utf-8
import sys
from os import path as os_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import *

admin.autodiscover()

urlpatterns = patterns('',
    (r'^ebioinfo/admin/', include(admin.site.urls)),
    url(r'^ebioinfo/i18n/setlang/$', 'django.views.i18n.set_language', name='change_language'),

    url(r'^ebioinfo/$', 'appsite.views.home', name='home'),
    url(r'^ebioinfo/app/', include('appsite.urls')),
    (r'^ebioinfo/accounts/', include('accounts.urls')),
    (r'^ebioinfo/courses/', include('courses.urls')),
    (r'^ebioinfo/enrollments/', include('enrollments.urls')),
    (r'^ebioinfo/institutions/', include('institutions.urls')),
    
    # plugins
    (r'^ebioinfo/genome-annotation/', include('plugins.genome_annotation.urls')),
    (r'^ebioinfo/calendar/', include('plugins.calendar.urls')),
)

if 'runserver' in sys.argv:
	urlpatterns += patterns('',
    	(r'^ebioinfo/admin_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': os_path.join(settings.PROJECT_PATH, 'admin_media'), 'show_indexes': True}),
    	(r'^ebioinfo/front_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': os_path.join(settings.PROJECT_PATH, 'media'), 'show_indexes': True}),
	)
