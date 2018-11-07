# coding: utf-8
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TissueKind(models.Model):
    code = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=32)
    
    class Meta:
        app_label = 'genome_annotation'
    
    def __unicode__(self):
        return self.name



class Tissue(models.Model):
    TYPE_C = (('n', 'Normal'), ('t', 'Tumoral'))
    symbol = models.CharField(_('symbol'), max_length=2, unique=True)
    type = models.CharField(_('type'), max_length=1, choices=TYPE_C)
    name = models.CharField(_('name'), max_length=32)
    kind = models.ForeignKey(TissueKind)
    est_qty = models.IntegerField(null=True)
    singlet_qty = models.IntegerField(null=True)
    contig_qty = models.IntegerField(null=True)

    class Meta:
        app_label = 'genome_annotation'
        verbose_name, verbose_name_plural = _('tissue'), _('tissues')
        ordering = ('name',)
    
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.get_type_display())

    @property
    def depth_avg(self):
        if self.contig_qty and self.contig_qty > 0:
            return round(float(self.est_qty-self.singlet_qty)/float(self.contig_qty),2)
        return u'N/A'


class Contig(models.Model):
    tissue = models.ForeignKey(Tissue, verbose_name=_('tissue'))
    name = models.CharField(max_length=64)
    base_qty = models.IntegerField()
    est_qty = models.IntegerField()
    sequence = models.TextField(blank=True)
    frequency = models.FloatField(null=True)
    
    class Meta:
        app_label = 'genome_annotation'
        verbose_name, verbose_name_plural = _('contig'), _('contigs')    
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
        