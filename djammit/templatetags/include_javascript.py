import os
import re
from django import template
from django.core import management
from djammit.finders import filefinder
from djammit import settings

register = template.Library()

class JavaScriptAssetsNode(template.Node):

    def __init__(self, compiled_js):
        self.compiled_js = compiled_js

    def render(self, context):
        return self.compiled_js


def get_template_name(path, base_path):
    extension = settings.JST_EXTENSION
    if not base_path:
        return os.path.basename(path)
    return re.sub(base_path + '(.*)' + extension, r"\1", path)

def compile_jst(paths):
    compiled = []
    namespace = settings.JST_NAMESPACE
    base_path = os.path.commonprefix(paths)
    for path in paths:
        content = open(path).read()
        content = content.replace('\n', '').replace("'", "\\\'")
        name = get_template_name(path, base_path)
        compiled.append(namespace + "['" + name + "'] = _.template('" + content + "');")
    # TODO Clean this shit up
    # JST file constants.
    JST_START = "(function(){"
    JST_END = "})();"
    setup_namespace = "window.JST = window.JST || {};"
    compiled = JST_START + setup_namespace + "".join(compiled) + JST_END
    return compiled

def compile_javascript(paths):
    static_url = settings.STATIC_URL
    static_root = settings.STATIC_ROOT
    if not static_root[-1] == '/':
        static_root += '/'
    compiled = []
    for path in paths:
        path = path.replace(static_root, '')
        compiled.append('<script src="' + static_url + path + '"></script>')
    # Temp hack:
    compiled.append('<script src="' + static_url + 'core.js"></script>')
    return "\n".join(compiled)

def remove_dups(paths):
    seen = set()
    unique = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique

def get_paths(packages):

    paths = []

    for package in packages:
        patterns = settings.JAVASCRIPTS[package]
        for pattern in patterns:
            paths.extend(filefinder(pattern))

    paths = remove_dups(paths)
    scripts = [path for path in paths if os.path.splitext(path)[1] == '.js']
    templates = [path for path in paths if os.path.splitext(path)[1] == '.jst']

    return (scripts, templates)

def run_collectstatic():
    management.call_command('collectstatic', interactive=False)

def package(compiled_jst):
    path = os.path.join(settings.STATIC_ROOT, 'core.js')
    f = open(path, 'w')
    f.write(compiled_jst)

def validate_packages(packages):
    for package in packages:
        if package not in settings.JAVASCRIPTS.keys():
            raise Exception("%s is not in your JAVASCRIPTS setting.", package)

def include_javascript(parser, token):
    bits = token.contents.split()
    validate_packages(bits[1:])
    packages = bits[1:] if len(bits) > 1 else settings.JAVASCRIPTS.keys()
    run_collectstatic()
    scripts, templates = get_paths(packages)
    compiled_js = compile_javascript(scripts)
    compiled_jst = compile_jst(templates)
    package(compiled_jst)
    return JavaScriptAssetsNode(compiled_js)
include_javascript = register.tag(include_javascript)

