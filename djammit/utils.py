def javascript_include_tag(sources):
    template = '<script type="text/javascript" src="%s"></script>'
    return "\n".join([template % source for source in sources])

def remove_dups(paths):
    seen = set()
    unique = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique
