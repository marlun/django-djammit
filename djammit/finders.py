import os

from django.conf import settings
from fnmatch import fnmatch

def filefinder(pattern):
    paths = []
    if '**' in pattern:
        folder, wild, pattern = pattern.partition('/**/')
        folder = os.path.join(settings.STATIC_ROOT, folder)
        for f in recursive_find_files(folder, pattern):
            paths.append(f)
    else:
        folder, pattern = os.path.split(pattern)
        folder = os.path.join(settings.STATIC_ROOT, folder)
        #print folder
        for f in find_files(folder, pattern):
            paths.append(f)
    return paths

def recursive_find_files(folder, pattern):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if fnmatch(f, pattern):
                yield os.path.join(root, f)

def find_files(folder, pattern):
    for entry in os.listdir(folder):
        if not os.path.isdir(entry) and fnmatch(entry, pattern):
            yield os.path.join(folder, entry)
