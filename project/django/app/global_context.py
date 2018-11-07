from django.conf import settings

def context(*args, **kwargs):
    return {'SITE_URL': settings.SITE_URL, 
            'LOGGED_IN_TIME_DELTA': settings.LOGGED_IN_TIME_DELTA}