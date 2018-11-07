# coding: utf-8
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from enrollments.models import Enrollment
from contigs import Contig, Tissue, TissueKind
from projects import Project


class PluginEnrollment(models.Model):
	enrollment = models.ForeignKey(Enrollment, unique=True, verbose_name=_('enrollment'))
	project = models.ForeignKey(Project, verbose_name=_('project'))
	tissue = models.ForeignKey(TissueKind, verbose_name=_('tissue'))
	date_added = models.DateTimeField(_('date added'), default=datetime.now)
	
	class Meta:
		app_label = 'genome_annotation'
		verbose_name, verbose_name_plural = _('plugin enrollment'), _('plugin enrollments')
		ordering = ('-date_added',)
	
	def save(self, *args, **kwargs):
	    if not self.id:
	        try:
	            ids_to_exclude = [o.tissue.id for o in PluginEnrollment.objects.filter(project=self.project, enrollment__course_class=self.enrollment.course_class)]
	            self.tissue = TissueKind.objects.exclude(id__in=ids_to_exclude)[0]
	        except IndexError:
	            self.tissue = TissueKind.objects.order_by('?')[0]

	    return super(PluginEnrollment, self).save(*args, **kwargs)
	
	def __unicode__(self):
	    return u'%s - %s' % (self.enrollment.user, self.project.name)
	
	def annotated_perc(self):
	    annotated = self.annotation_set.filter(Q(status=Annotation.VALIDATED) | Q(status=Annotation.EXCLUDED)).count()
	    total = Contig.objects.filter(tissue__kind=self.tissue).count()
	    return round(float(annotated * 100) / float(total), 2)
	
	def get_last_submission(self):
	    try:
	        ret = self.submission_set.filter(date_submitted__isnull=False).order_by('-id')[0]
	    except:
	        ret = None
	    return ret


class Annotation(models.Model):
	PENDING, VALIDATED, EXCLUDED, TO_REVIEW = range(4)
	STATUS_CHOICES = ((PENDING, _('Pending')), 
					(VALIDATED, _('Validated')),  
					(EXCLUDED, _('Excluded')), 
					(TO_REVIEW, _('To review')),)
	
	enrollment = models.ForeignKey(PluginEnrollment)
	contig = models.ForeignKey(Contig)
	gene_symbol = models.CharField(max_length=32, blank=True)
	gene_map = models.CharField(max_length=32, blank=True)
	refseq = models.CharField(max_length=32, blank=True)
	unigene = models.CharField(max_length=32, blank=True)
	status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
	is_snp = models.BooleanField(default=False)
	is_paralog = models.BooleanField(default=False)
	is_ortolog = models.BooleanField(default=False, db_column='is_multiple_chr')
	is_alt_splice = models.BooleanField(default=False)
	obs = models.TextField(blank=True)
	annotation = models.TextField(blank=True)
	date_added = models.DateTimeField(auto_now_add=datetime.now)
	
	class Meta:
		app_label = 'genome_annotation'
		verbose_name, verbose_name_plural = _('annotation'), _('annotations')
		unique_together = ('enrollment', 'contig',)

	def __unicode__(self):
		return u'%s' % self.contig.name
