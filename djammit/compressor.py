import os
import re

from djammit import settings

JST_START = "(function(){"
JST_END = "})();"

def readfile(path):
    return open(path, 'r').read()

def concatenate(paths):
    return map(readfile, paths)

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
    # JST file constants.
    setup_namespace = "%s = %s || {};" % (settings.JST_NAMESPACE, settings.JST_NAMESPACE)
    compiled = JST_START + setup_namespace + "".join(compiled) + JST_END
    return compiled

def compile_js(paths):
    compiled = ""
    scripts = [path for path in paths if os.path.splitext(path)[1] == '.js']
    templates = [path for path in paths if os.path.splitext(path)[1] == '.jst']
    if settings.DEBUG:
        compiled += compile_jst(templates)
    else:
        compiled += concatenate(scripts) + compile_jst(templates)
    print compiled
    return compiled

