from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEBUG = getattr(settings, 'DEBUG', False)

if not hasattr(settings, 'STATIC_URL'):
    raise ImproperlyConfigured("STATIC_URL needs to be set in your settings.py file")
STATIC_URL = settings.STATIC_URL

if not hasattr(settings, 'STATIC_ROOT'):
    raise ImproperlyConfigured("STATIC_ROOT needs to be set in your settings.py file")
STATIC_ROOT = settings.STATIC_ROOT

TEMPLATE_EXTENSION = getattr(settings, 'DJAMMIT_TEMPLATE_EXTENSION', '.jst')
TEMPLATE_NAMESPACE = getattr(settings, 'DJAMMIT_TEMPLATE_NAMESPACE', 'window.JST')

# no bundled template function, so we might as well use Underscore's.
# set to False to completely avoid that step
TEMPLATE_FUNCTION = getattr(settings, 'DJAMMIT_TEMPLATE_FUNCTION', '_.template')

JAVASCRIPTS = getattr(settings, 'DJAMMIT_JAVASCRIPTS', {})

#
# Add a setting to use a collect command and make the default a bit cleverer
#
if not hasattr(settings, 'DJAMMIT_COLLECT_COMMAND'):
    # try using either django-staticfiles or django.contrib.staticfiles
    apps = getattr(settings, 'INSTALLED_APPS', [])
    if 'staticfiles' in apps:
        COLLECT_COMMAND = 'build_static'
    elif 'django.contrib.staticfiles' in apps:
        COLLECT_COMMAND = 'collectstatic'
else:
    COLLECT_COMMAND = settings.DJAMMIT_COLLECT_COMMAND

#
# Allow the user to override the default output directory
#
ROOT = getattr(settings, 'DJAMMIT_ROOT', STATIC_ROOT)
