# coding: utf-8
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from projects import Project
from annotation import PluginEnrollment
from courses.models import Course


class Question(models.Model):
    course = models.ForeignKey(Course, verbose_name=_('course'))
    project = models.ForeignKey(Project, verbose_name=_('project'))
    text = models.TextField(_('question'))
    order = models.IntegerField(_('order'), default=0)
    date_added = models.DateTimeField(_('date added'), default=datetime.now)
    
    class Meta:
        app_label = 'genome_annotation'
        ordering = ('order',)
        verbose_name, verbose_name_plural = _('question'), _('questions')
    
    def __unicode__(self):
        return u'%s - %s...' % (self.project, self.text[:30])


class Answer(models.Model):
    plugin_enrollment = models.ForeignKey(PluginEnrollment)
    question = models.ForeignKey(Question)
    text = models.TextField()
    #TODO: adicionar campo para upload do arquivo
    date_added = models.DateTimeField(_('date added'), default=datetime.now)
    
    class Meta:
        app_label = 'genome_annotation'
        verbose_name, verbose_name_plural = _('answer'), _('answers')
    
    def __unicode__(self):
        return u'%s - %s' % (self.plugin_enrollment, self.text)


class UserFile(models.Model):
    answer = models.ForeignKey(Answer)
    file = models.FileField(upload_to='userfiles')
    date_added = models.DateTimeField(_('date added'), default=datetime.now)

    class Meta:
        app_label = 'genome_annotation'
        verbose_name, verbose_name_plural = _('user file'), _('files')

    def __unicode__(self):
        return self.file.name
        
    def filename(self):
        return self.file.name.split('/')[-1]