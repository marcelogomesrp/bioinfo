import os
from django.utils.importlib import import_module
from signals import *
from base import manager 
from options import BasePlugin

LOADING = False

def autodiscover():
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    path = os.path.dirname(__file__)

    for entry in os.listdir(path):
        if os.path.isdir(os.path.join(path,entry)):
            try:
                mod = import_module('plugins.%s' % entry)
            except Exception, e:
                continue
            
            try:
                app_path = mod.__path__
            except AttributeError, e:
                continue
            try:
                imp.find_module('plugin', app_path)
            except ImportError, e:
                continue
            
            import_module("plugins.%s.plugin" % entry)

    LOADING = False

autodiscover()