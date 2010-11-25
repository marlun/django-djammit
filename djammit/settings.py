from django.conf import settings

DEBUG = getattr(settings, 'DEBUG', False)

if not hasattr(settings, 'STATIC_URL'):
    raise Exception("STATIC_URL needs to be set in your settings.py file")
STATIC_URL = settings.STATIC_URL

if not hasattr(settings, 'STATIC_ROOT'):
    raise Exception("STATIC_ROOT needs to be set in your settings.py file")
STATIC_ROOT = settings.STATIC_ROOT

JST_EXTENSION = getattr(settings, 'JST_EXTENSION', '.jst')

JST_NAMESPACE = getattr(settings, 'JST_NAMESPACE', 'JST')

JAVASCRIPTS = getattr(settings, 'JAVASCRIPTS', {})
