# coding: utf-8
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_detail, object_list
from django.utils.translation import ugettext_lazy as _
from institutions.models import Institution
from util.views import create_object
from models import Course, Class


def list_classes_by_institution(request, institution_id):
    ''' List all courses from a institution '''
    institution = get_object_or_404(Institution, id=institution_id)

    return object_list(request,
            template_name='courses/list_classes.html',
            queryset=Class.active.filter(department__institution=institution),
            extra_context={'institution': institution})


def class_detail(request, class_id):
    if request.method == 'POST':
        ''' Enroll current user to the course '''
        if not request.user.is_authenticated():
            return redirect('class_detail', args=(class_id,))
        course_class = get_object_or_404(Class.active, id=class_id)
        
        try:
            class_enrollment = course_class.enroll_user(request.user)
        except Exception, e:
            return redirect('already_enrolled')
        
        next_urls = []        
        for p in course_class.active_plugins:
            if hasattr(p, 'enrollment_url'):
                next_urls.append(p.enrollment_url)
        
        if next_urls:
            return redirect(next_urls.pop(), classenrollment_id=class_enrollment.id)
        
        return redirect('enrollment_success')
    
    return object_detail(request,
            queryset=Class.active,
            object_id=class_id)


def class_permalink(request, code):
    course_class = get_object_or_404(Class.active, code=code.lower())
    return class_detail(request, course_class.id)
    
