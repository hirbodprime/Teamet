import re


def slugify(name):
    name = name.lower().strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_-]+', '-', name)
    name = re.sub(r'^-+|-+$', '', name)
    return name


def generate_path(parent, name):
    if parent:
        return f'{parent.path}/{slugify(name)}'
    
    return slugify(name)
    