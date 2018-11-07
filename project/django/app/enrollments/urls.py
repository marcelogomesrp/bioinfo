from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views

urlpatterns = patterns('',
    url(r'^already-enrolled/$', direct_to_template, 
        {'template': 'enrollments/already_enrolled.html'}, name='already_enrolled'),
    url(r'^success/$', direct_to_template, 
        {'template': 'enrollments/enrollment_success.html'}, name='enrollment_success'),
    url(r'^user/$', views.user_enrollments, name='user_enrollments'),
    url(r'^dashboard/(?P<classenrollment_id>\d+)/$', views.student_dashboard, name='enrollment_dashboard'),
    url(r'^stats/(?P<classenrollment_id>\d+)/$', views.student_stats, name='student_stats'),
    url(r'^instructor/(?P<class_id>\d+)/stats/$', views.instructor_stats, name='instructor_stats'),
    url(r'^instructor/(?P<class_id>\d+)/$', views.instructor_dashboard, name='instructor_dashboard'),
    url(r'^manage/(?P<class_id>\d+)/$', views.manage_enrollments, name='manage_enrollments'),
    url(r'^approve/(?P<class_id>\d+)/(?P<enrollment_id>\d+)/$', views.approve_enrollment, name='approve_enrollment'),
    url(r'^remove/(?P<class_id>\d+)/(?P<enrollment_id>\d+)/$', views.remove_enrollment, name='remove_enrollment'),
    url(r'^pending/$', direct_to_template, 
        {'template': 'enrollments/pending_approval.html'}, name='pending_approval'),
)
