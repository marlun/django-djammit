def javascript_include_tag(sources):
    template = '<script type="text/javascript" src="%s"></script>'
    return "\n".join([template % source for source in sources])

def remove_dups(iterable):
    uniqs = set(iterable)
    return [val for val in iterable if val in uniqs]
