from django.db.models import signals
from django.utils.importlib import import_module
from models import Plugin

def add_db_plugin(sender, app, *args, **kwargs):
    #TODO: refatorar isso
    app_name = sender.__name__
    plugin_id = ''
    if app_name.startswith('plugins.'):
        try:
            modul = 'plugins.%s.plugin' % app_name.split('.')[1]
            import_module(modul)
        except:
            pass
        if not Plugin.objects.filter(plugin_id=plugin_id).count():
            print 'abriu %s' % app_name
            Plugin.objects.create(name='x', plugin_id=plugin_id)

signals.post_syncdb.connect(add_db_plugin)