# coding: utf-8
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from courses.models import Class as CourseClass


class Class(models.Model):
    course_class = models.ForeignKey(CourseClass, verbose_name=_('course'), 
                                        related_name='calendarclass_set')
    title = models.CharField(_('title'), max_length=128)
    professor = models.CharField(_('professor'), max_length=32, blank=True)
    date = models.DateTimeField(_('date'))
    classroom = models.CharField(_('class room'), max_length=12, blank=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('class'), _('classes')
        ordering = ('date',)
    
    def __unicode__(self):
        return self.title