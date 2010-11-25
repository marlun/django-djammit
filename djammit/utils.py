def javascript_include_tag(sources):
    tags = []
    for source in sources:
        tags.append('<script src="%s"></script>' % source)
    return "\n".join(tags)

def remove_dups(paths):
    seen = set()
    unique = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique

