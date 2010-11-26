import os

from djammit import settings

JST_START = "(function(){"
JST_END = "})();"

def readfile(path):
    return open(path, 'r').read()

def compile_js(paths):
    return "".join(map(readfile, paths))

def get_template_name(path, base_path):
    extension = settings.JST_EXTENSION

    name = os.path.basename(path)

    if not base_path:
        return name

    # removing the extension
    return name.replace(extension, "")

def compile_jst(paths):
    bits = {
        'namespace': settings.JST_NAMESPACE,
    }
    namespace_setup = "%(namespace)s = %(namespace)s || {};" % bits

    # do we generate a wrapper function or just pass the string along?
    if settings.JST_FUNCTION:
        bits['template_func'] = settings.JST_FUNCTION
        format = "%(namespace)s['%(name)s'] = %(template_func)s('%(template)s');"
    else:
        format = "%(namespace)s['%(name)s'] = '%(template)s';"

    base_path = os.path.commonprefix(paths)

    compiled = []
    for path in paths:
        f = open(path)
        try:
            bits['template'] = f.read().replace('\n', '').replace("'", r"\'")
            bits['name'] = get_template_name(path, base_path)

            compiled.append(format % bits)
        finally:
            f.close()

    # JST file constants.
    return JST_START + namespace_setup + " ".join(compiled) + JST_END

def compile_assets(paths):
    compiled = ""

    # separate the different kinds of assets
    assets = {
        '.js': [],
        '.css': [],
        settings.JST_EXTENSION: [],
    }

    for path in paths:
        for t in assets.keys():
            if path.endswith(t):
                assets[t].append(path)
                break

    # compile templates
    compiled += compile_jst(assets[settings.JST_EXTENSION])

    # compile scripts
    if not settings.DEBUG:
        compiled += compile_js(assets['.js'])
    return compiled

