from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Institution(models.Model):
    name = models.CharField(_('name'), max_length=128)
    short_name = models.CharField(_('short name'), max_length=10)
    city = models.CharField(_('city'), max_length=64)
    state = models.CharField(_('state'), max_length=2)

    class Meta:
        verbose_name, verbose_name_plural = _('institution'), _('institutions')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Department(models.Model):
    institution = models.ForeignKey(Institution, verbose_name=_('institution'))
    name = models.CharField(_('name'), max_length=64)

    class Meta:
        verbose_name, verbose_name_plural = _('department'), _('departments')
        ordering = ('name',)

    def __unicode__(self):
        return self.name
