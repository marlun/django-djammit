from django.conf import settings
from exceptions import ConfigurationError

DEBUG = getattr(settings, 'DEBUG', False)

if not hasattr(settings, 'STATIC_URL'):
    raise ConfigurationError("STATIC_URL needs to be set in your settings.py file")
STATIC_URL = settings.STATIC_URL

if not hasattr(settings, 'STATIC_ROOT'):
    raise ConfigurationError("STATIC_ROOT needs to be set in your settings.py file")
STATIC_ROOT = settings.STATIC_ROOT

JST_EXTENSION = getattr(settings, 'JST_EXTENSION', '.jst')

JST_NAMESPACE = getattr(settings, 'JST_NAMESPACE', 'window.JST')

JAVASCRIPTS = getattr(settings, 'JAVASCRIPTS', {})

# no bundled template function, so we might as well use Underscore's.
# set to False to completely avoid that step
JST_FUNCTION = getattr(settings, 'JST_FUNCTION', '_.template')

#
# Add a setting to use a collect command and make the default a bit cleverer
#
if not hasattr(settings, 'DJAMMIT_COLLECT_COMMAND'):
    # try using either django-staticfiles or django.contrib.staticfiles
    apps = getattr(settings, 'INSTALLED_APPS', [])
    if 'staticfiles' in apps:
        DJAMMIT_COLLECT_COMMAND = 'build_static'
    elif 'django.contrib.staticfiles' in apps:
        DJAMMIT_COLLECT_COMMAND = 'collectstatic'
else:
    DJAMMIT_COLLECT_COMMAND = settings.DJAMMIT_COLLECT_COMMAND
