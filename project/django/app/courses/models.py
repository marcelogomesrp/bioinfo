# coding: utf-8
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from institutions.models import Institution, Department
from plugins import manager as plugin_manager
from plugins.models import Plugin
import managers


class Course(models.Model):
    name = models.CharField(_('name'), max_length=64)
    short_description = models.TextField(_('short description'))
    full_descritption = models.TextField(_('full description'))
    plugins = models.ManyToManyField(Plugin, null=True, blank=True)

    class Meta:
        verbose_name, verbose_name_plural = _('course'), _('courses')
    
    def __unicode__(self):
        return self.name

class Class(models.Model):
    course = models.ForeignKey(Course, verbose_name=_('course'))
    instructor = models.ForeignKey(User, verbose_name=_('Instructor'))
    department = models.ForeignKey(Department, verbose_name=_('department'))
    code = models.CharField(_('code'), max_length=16, unique=True)
    name = models.CharField(_('name'), max_length=64)
    date_added = models.DateTimeField(_('date added'), default=datetime.now)
    short_description = models.TextField(_('short description'))
    full_descritption = models.TextField(_('full description'))
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField()
    enrollment_start_date = models.DateField(default=datetime.now)
    enrollment_end_date = models.DateField()

    objects = models.Manager()
    active = managers.ActiveClassManager()

    class Meta:
        verbose_name, verbose_name_plural = _('class'), _('classes')
        ordering = ('name',)

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        ''' Código da disciplina deve ser sempre minúsculo '''
        if self.code:
            self.code = self.code.lower()
        return super(Class, self).save(*args, **kwargs)
        
    @property
    def institution(self):
        return self.department.institution

    def enroll_user(self, user):
        ''' Matricula o usuário no curso '''
        from enrollments.models import Enrollment
        # check if user is the instructor\
        # if self.instructor == user:
        #     raise Exception('''You are already enrolled in this class as instructor''')
        
        # check if user is already attending to this course
        if self.enrollment_set.filter(user=user).count():
            raise Exception('You are already enrolled in this class')
        
        return Enrollment.objects.create(user=user, course_class=self)
    
    @property
    def active_plugins(self):
        plugin_set = dict(plugin_manager.get_list())
        self._active_plugins = [plugin_set[plugin.plugin_id] for plugin in self.course.plugins.all() \
                                if plugin.plugin_id in plugin_manager.get_ids()]
        return self._active_plugins
    
    @property
    def enrolled_users(self):
        return User.objects.filter(enrollment__course_class=self, enrollment__is_approved=True)
    
    @property
    def pending_users(self):
        return User.objects.filter(enrollment__course_class=self, enrollment__is_approved=False)