# coding: utf-8
from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from util.email import EmailMessage
from annotation import PluginEnrollment


class Submission(models.Model):
    plugin_enrollment = models.ForeignKey(PluginEnrollment)
    title = models.CharField(blank=True, null=True, max_length=128)
    text = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now)
    date_submitted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        app_label = 'genome_annotation'        
        verbose_name, verbose_name_plural = _('submission'), _('submissions')
    
    def save(self, *args, **kwargs):
        self.last_update = datetime.now()
        return super(Submission, self).save(*args, **kwargs)
    
    def submit(self):
        self.date_submitted = datetime.now()
        self.save()
        message = EmailMessage(self.plugin_enrollment.enrollment.user.email, 
                    _('Your resume has been submitted'),
                    'genome_annotation/submission/email.txt', {})
        message.send()

    
    def __unicode__(self):
        return u'%s' % self.title
        
    def get_ordered_author_institution(self):
        a = []
        i = []
                
        for author in self.author_set.all():
            if not author.institution in i:
                i.append(author.institution)
            author.index = i.index(author.institution) + 1
            a.append(author)
        
        return (a, i)
    
    def pdf_url(self):
        return reverse('submission_instructor_pdf_download', kwargs={
                'submission_id': self.id, 
        })

class Institution(models.Model):
    submission = models.ForeignKey(Submission)
    name = models.CharField(max_length=64,
                    help_text=u'Ex: USP - Universidade de São Paulo')
    
    class Meta:
        app_label = 'genome_annotation'
        ordering = ('name',)     
        verbose_name, verbose_name_plural = _('institution'), _('institutions')
    
    def __unicode__(self):
        return self.name


class Author(models.Model):
    submission = models.ForeignKey(Submission)
    institution = models.ForeignKey(Institution)
    name = models.CharField(_('name'), max_length=32,
                    help_text=_('Eg: SILVA-JR, WA'))
    email = models.EmailField(_('e-mail'))
    ordering = models.IntegerField(_('ordering'), default=0)
    
    class Meta:
        app_label = 'genome_annotation'        
        ordering = ('ordering', 'name',)
        verbose_name, verbose_name_plural = _('author'), _('authors')
    
    def __unicode__(self):
        return self.name