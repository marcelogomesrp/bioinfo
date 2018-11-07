from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import plugins

class CalendarPlugin(plugins.BasePlugin):
    plugin_id = 'calendar'
    verbose_name = _('Calendar')
    order = 0
    enrollment_url = None
    
plugins.manager.register(CalendarPlugin)