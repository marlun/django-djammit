import os
from django import template
from django.core import management
from django.core.exceptions import ImproperlyConfigured
from djammit.finders import filefinder
from djammit.compressor import compile_assets
from djammit.utils import javascript_include_tag, remove_dups

from djammit.settings import ROOT, JAVASCRIPTS, TEMPLATE_EXTENSION, \
    STATIC_ROOT, STATIC_URL, COLLECT_COMMAND

register = template.Library()

class JavaScriptAssetsNode(template.Node):

    def __init__(self, tags):
        self.tags = tags

    def render(self, context):
        return self.tags


def pack(compiled, package):
    f = open(os.path.join(ROOT, package + ".js"), 'w')
    f.write(compiled)

def compile_packages(packages):
    for package in packages:
        paths = get_paths(package)
        compiled = compile_assets(paths)
        pack(compiled, package)

def get_paths(package):
    paths = []
    patterns = JAVASCRIPTS[package]
    for pattern in patterns:
        paths.extend(filefinder(pattern))

    return remove_dups(paths)

def get_urls_for(package):
    urls = []
    base_path = STATIC_ROOT + '/'

    paths = get_paths(package)

    scripts = [p.replace(base_path, '') for p in paths if p.endswith('.js')]
    for path in scripts:
        urls.append(STATIC_URL + path)

    templates = [path for path in paths if path.endswith(TEMPLATE_EXTENSION)]
    if len(templates):
        urls.append(STATIC_URL + package + ".js")

    return urls

def get_tags(packages):
    urls = [get_urls_for(package) for package in packages]
    urls = reduce(lambda x,y: x+y, urls) # flatten the list of lists
    return javascript_include_tag(urls)

def run_collectstatic():
    management.call_command(COLLECT_COMMAND, interactive=False)

def validate_packages(packages):
    for package in packages:
        if package not in JAVASCRIPTS.keys():
            raise ImproperlyConfigured("%s is not in your DJAMMIT_JAVASCRIPTS setting." % package)

def include_javascript(parser, token):
    bits = token.contents.split()
    validate_packages(bits[1:])
    packages = bits[1:] if len(bits) > 1 else JAVASCRIPTS.keys()

    run_collectstatic()

    compile_packages(packages)

    tags = get_tags(packages)

    return JavaScriptAssetsNode(tags)

include_javascript = register.tag(include_javascript)

