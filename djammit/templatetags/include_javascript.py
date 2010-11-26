import os
from django import template
from django.core import management
from djammit import settings
from djammit.finders import filefinder
from djammit.compressor import compile_assets
from djammit.utils import javascript_include_tag, remove_dups
from djammit.exceptions import ConfigurationError

register = template.Library()

class JavaScriptAssetsNode(template.Node):

    def __init__(self, tags):
        self.tags = tags

    def render(self, context):
        return self.tags


def pack(compiled, package):
    f = open(os.path.join(settings.STATIC_ROOT, package + ".js"), 'w')
    f.write(compiled)

def compile_packages(packages):
    for package in packages:
        paths = get_paths(package)
        compiled = compile_assets(paths)
        pack(compiled, package)

def get_paths(package):
    paths = []
    patterns = settings.JAVASCRIPTS[package]
    for pattern in patterns:
        paths.extend(filefinder(pattern))

    return remove_dups(paths)

def get_urls_for(package):
    urls = []
    base_path = settings.STATIC_ROOT + '/'

    paths = get_paths(package)

    scripts = [p.replace(base_path, '') for p in paths if p.endswith('.js')]
    for path in scripts:
        urls.append(settings.STATIC_URL + path)

    templates = [path for path in paths if path.endswith(settings.JST_EXTENSION)]
    if len(templates):
        urls.append(settings.STATIC_URL + package + ".js")

    return urls

def get_tags(packages):
    urls = [get_urls_for(package) for package in packages]
    urls = reduce(lambda x,y: x+y, urls) # flatten the list of lists
    return javascript_include_tag(urls)

def run_collectstatic():
    command = settings.DJAMMIT_COLLECT_COMMAND
    management.call_command(command, interactive=False)

def validate_packages(packages):
    for package in packages:
        if package not in settings.JAVASCRIPTS.keys():
            raise ConfigurationError("%s is not in your JAVASCRIPTS setting.", package)

def include_javascript(parser, token):
    bits = token.contents.split()
    validate_packages(bits[1:])
    packages = bits[1:] if len(bits) > 1 else settings.JAVASCRIPTS.keys()

    run_collectstatic()

    compile_packages(packages)

    tags = get_tags(packages)

    return JavaScriptAssetsNode(tags)

include_javascript = register.tag(include_javascript)

