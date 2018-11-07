from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^add/$', views.add_institution, name='add_institution'),
    url(r'^department/add/$', views.add_department, name='add_department'),
    url(r'^list/$', views.list_institutions, name='list_institutions'),
    url(r'^view/(?P<object_id>\d+)/$', views.view_institution, name='view_institution'),
)
