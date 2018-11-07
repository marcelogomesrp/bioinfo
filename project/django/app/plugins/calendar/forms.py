# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Class


class AddClassForm(forms.ModelForm):
    class Meta:
        model = Class
        exclude = ('course_class',)