# coding: utf-8
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from enrollments.decorators import class_enrollment_required
from plugins.util import get_class_enrollment
from courses.models import Class as CourseClass
from forms import AddClassForm
from models import Class


@login_required
@class_enrollment_required
def list_classes(request, classenrollment_id):
    class_enrollment = get_class_enrollment(request.user, classenrollment_id)
        
    return direct_to_template(request,
                template='calendar/list_classes.html',
                extra_context={
                    'object_list': Class.objects.filter(course_class=class_enrollment.course_class),
                    'class_enrollment': class_enrollment,
                })
                
@login_required
def instructor_list_classes(request, class_id):
    course_class = get_object_or_404(CourseClass, pk=class_id)

    return direct_to_template(request,
                template='calendar/instructor_list_classes.html',
                extra_context={
                    'object_list': Class.objects.filter(course_class=course_class),
                    'class': course_class,
                })
                

@login_required
def add_class(request, class_id):
    course_class = get_object_or_404(CourseClass, pk=class_id)
    
    if request.method == 'POST':
        form = AddClassForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course_class = course_class
            obj.save()
            
            messages.info(request, _('Class "%s" added' % obj.title))
            
            return redirect('calendar_instructor_list_classes', class_id=class_id)
            
    else:
        form = AddClassForm()
    
    return direct_to_template(request,
                template='calendar/add_class.html',
                extra_context={
                    'object_list': Class.objects.filter(course_class=course_class),
                    'class': course_class,
                    'form': form,
                })