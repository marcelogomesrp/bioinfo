# coding: utf-8
from django import forms
from models import PluginEnrollment

class ProjectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return u'%(project_name)s (%(available)d available)' % {
            'project_name': obj.name,
            'available': obj.get_available_seats(self.course_class),
        }