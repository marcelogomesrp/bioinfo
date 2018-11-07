from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import plugins

class GenomeAnnotationPlugin(plugins.BasePlugin):
    plugin_id = 'genome_annotation'
    verbose_name = _('Activities')
    order = 0
    enrollment_url = 'genome_annotation_plugin_enrollment'
    
plugins.manager.register(GenomeAnnotationPlugin)