# coding: utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from courses.models import Class
from institutions.models import Institution


def home(request):
    if request.user.is_authenticated():
        return redirect('dashboard')
    
    return render_to_response('appsite/home.html', {
                                    'institutions': Institution.objects.order_by('name'),
                                },
                                context_instance=RequestContext(request))
                         
       
def dashboard(request):
    class_list = Class.active.select_related('course', 'instructor').all()
    
    return render_to_response('appsite/dashboard.html', {
                                'class_list': class_list
                                },
                                context_instance=RequestContext(request))