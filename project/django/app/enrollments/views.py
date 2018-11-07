from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _
from courses.models import Class
from decorators import class_enrollment_required
from plugins.decorators import plugin_enrollment_required
from models import Enrollment


@login_required
@class_enrollment_required
@plugin_enrollment_required
def student_stats(request, classenrollment_id):
    ''' List logged in time of all enrolled students '''
    class_enrollment = get_object_or_404(Enrollment.approved, pk=classenrollment_id)
    
    return direct_to_template(request,
            template='enrollments/student_stats.html',
            extra_context={'class_enrollment': class_enrollment})

@login_required
def instructor_stats(request, class_id):
    ''' List logged in time of all enrolled students '''
    course_class = get_object_or_404(Class, pk=class_id)

    return direct_to_template(request,
            template='enrollments/instructor_stats.html',
            extra_context={'class': course_class})


@login_required
def user_enrollments(request):
    ''' List all courses which the current user is enrolled '''
    return object_list(request,
            template_name='enrollments/user_enrollments.html',
            queryset=request.user.enrollment_set.all())


@login_required
@class_enrollment_required
@plugin_enrollment_required
def student_dashboard(request, classenrollment_id):
    return object_detail(request,
            queryset=Enrollment.approved.select_related('class').filter(user=request.user),
            object_id=classenrollment_id,
            template_object_name='class_enrollment',
            template_name='enrollments/student_dashboard.html',
            )


@login_required
def instructor_dashboard(request, class_id):
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    
    return direct_to_template(request,
                              template='enrollments/instructor_dashboard.html',
                              extra_context={'class': course_class})
                        

@login_required
def manage_enrollments(request, class_id):
  course_class = get_object_or_404(request.user.class_set, pk=class_id)
  
  return direct_to_template(request,
                            template='enrollments/manage_enrollments.html',
                            extra_context={'class': course_class})

@login_required
def approve_enrollment(request, class_id, enrollment_id):
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    e = course_class.enrollment_set.get(pk=enrollment_id)
    e.is_approved = True
    e.save()
    e.notify_user()
    
    messages.info(request, _('Enrollment approved for "%s"' % e.user))
    
    return redirect('manage_enrollments', class_id=course_class.id)

@login_required
def remove_enrollment(request, class_id, enrollment_id):
    course_class = get_object_or_404(request.user.class_set, pk=class_id)
    e = course_class.enrollment_set.get(pk=enrollment_id)
    messages.info(request, _('Enrollment removed for "%s"' % e.user))
    e.delete()

    return redirect('manage_enrollments', class_id=course_class.id)