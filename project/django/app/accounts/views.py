# coding: utf-8
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list
from models import UserProfile


def view_account(request, uuid):
    user_profile = get_object_or_404(UserProfile, uuid=uuid)
    
    return render_to_response('accounts/view_account.html', locals(), 
                context_instance=RequestContext(request))


def list_accounts(request):
    return object_list(request, queryset=User.objects.all(),
                template_name='accounts/list_accounts.html')


def logout(request):
    auth_logout(request)
    messages.info(request, _('Your session has been closed'))
    return redirect('home')


def login(request, invalid=False):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(username=username, password=password)
    
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('home')
            else:
                return redirect('disabled_account')
        else:
            return redirect('invalid_login')

    return render_to_response('accounts/login.html', locals(),
                context_instance=RequestContext(request))


def update_logged_in_time(request):
    from enrollments.models import Enrollment
    
    account = request.user.get_profile()
    
    if not account.get_logged_in_time_hash() == request.POST.get('key', ''):
        return HttpResponse('failed')
    
    account.logged_in_time += settings.LOGGED_IN_TIME_DELTA
    account.save()
    
    if request.POST.get('enrollment_id'):
        enrollment = Enrollment.objects.get(pk=int(request.POST.get('enrollment_id')))
        enrollment.logged_in_time += settings.LOGGED_IN_TIME_DELTA
        enrollment.save()
        
    return HttpResponse(account.get_logged_in_time_hash())