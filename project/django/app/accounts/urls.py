# coding: utf-8
from django.conf.urls.defaults import *
from django.contrib.auth.views import password_change, password_change_done
from forms import RegistrationWizard, UserProfileForm, UserLoginForm


urlpatterns = patterns('accounts.views',
    url(r'^change-password/$', password_change, 
        {'template_name': 'accounts/change_password.html'}, name='change_password'),
    url(r'^password-changed/$', password_change_done, 
        {'template_name': 'accounts/password_changed.html'}, name='password_change_done'),
    url(r'^login/$', 'login', name='login'),
    url(r'^login/invalid/$', 'login', {'invalid': True}, name='invalid_login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^view/$', 'view_account', name='view_account'),
	url(r'^registration/$', RegistrationWizard([UserProfileForm, UserLoginForm]),
        name='registration'),	
    url(r'^list/$', 'list_accounts', name='list_accounts'),
    url(r'^tick/$', 'update_logged_in_time', name='update_logged_in_time'),

)
