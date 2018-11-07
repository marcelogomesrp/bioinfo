# coding: utf-8
from django.contrib import admin
from models import Class

class ClassAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'professor')

admin.site.register(Class, ClassAdmin)