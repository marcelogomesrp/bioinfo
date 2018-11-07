# coding: utf-8
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from courses.models import Course


class Project(models.Model):
    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'), blank=True)
    date_added = models.DateTimeField(default=datetime.now)
    
    class Meta:
        app_label = 'genome_annotation'
        verbose_name, verbose_name_plural = _('project'), _('projects')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
    @property
    def limit(self):
        ''' 
        Número de vagas disponíveis para este curso (que no caso é o nro
        de tecidos diferentes) 
        '''
        from contigs import TissueKind
        return TissueKind.objects.count() + 3
    
    def get_available_seats(self, course_class):
	    from annotation import PluginEnrollment
	    return self.limit - PluginEnrollment.objects.filter(enrollment__course_class=course_class, project=self).count()
