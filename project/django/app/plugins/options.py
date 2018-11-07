from django.core.urlresolvers import reverse
from django.db import models


class BasePlugin(object):
    plugin_id = ''
    verbose_name, verbose_name_plural = '', ''
    order = 0
    
    @property
    def menu_template(self): 
        return '%s/menu.html' % self.plugin_id