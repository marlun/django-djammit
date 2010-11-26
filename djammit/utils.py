def javascript_include_tag(sources):
    tags = []
    for source in sources:
        tags.append('<script type="text/javascript" src="%s"></script>' % source)
    return "\n".join(tags)

