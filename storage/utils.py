import re


def slugify(name):
    name = name.lower().strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_-]+', '-', name)
    name = re.sub(r'^-+|-+$', '', name)
    return name


def get_path_depth(parent, name):
    if parent:
        return f'{parent.path}/{slugify(name)}', 1
    
    return slugify(name), 0


def check_depth(parent):
    if not parent:
        return True
    
    return parent.depth == 0
    