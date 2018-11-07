from models import Plugin

class PluginManager(object):
    def __init__(self):
        self._registry = {}
    
    def register(self, plugin_class):
        plugin_id = getattr(plugin_class, 'plugin_id')
        
        if not plugin_id in self._registry:
            self._registry[plugin_id] = plugin_class()
            self._save_to_db(plugin_name=getattr(plugin_class, 'verbose_name'), 
                            plugin_id=plugin_id)
                                
    def get_list(self):
        if not getattr(self, '_ordered_plugin_list', None):
            self._ordered_plugin_list = sorted(self._registry.items(), key=lambda x: x[1].order)
        return self._ordered_plugin_list
    
    def get_ids(self):
        return self._registry.keys()
    
    def _save_to_db(self, plugin_name, plugin_id):
        try:
            if not Plugin.objects.filter(plugin_id=plugin_id):
                Plugin.objects.create(name=plugin_id, plugin_id=plugin_id)
        except:
            pass
manager = PluginManager()
