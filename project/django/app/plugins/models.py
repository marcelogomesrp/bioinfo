from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Plugin(models.Model):
    name = models.CharField(max_length=64)
    date_added = models.DateTimeField(default=datetime.now)
    plugin_id = models.CharField(max_length=32, unique=True)
    
    class Meta:
        verbose_name, verbose_name_plural = _('plugin'), _('plugins')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
