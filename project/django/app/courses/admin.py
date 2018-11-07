from django.contrib import admin
from models import Course, Class


class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('plugins',)

admin.site.register(Class)
admin.site.register(Course, CourseAdmin)