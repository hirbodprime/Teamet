import re


def slugify(name):
    name = name.lower().strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_-]+', '-', name)
    name = re.sub(r'^-+|-+$', '', name)
    return name
