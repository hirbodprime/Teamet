from django.conf import settings


def get_depth(parent, file_field, user):
    if not parent:
        return 0
    elif parent.parent_folder:
        return 2
    return 1


def get_path(parent, file_field, user):
    if not parent:
        return f'{file_field.name}'
    return f'{parent.path}/{file_field.name.split("/")[-1]}'


def get_new_name(name, parent):
    if not parent:
        return name
    file_name = name.split('/')[-1]
    new_name = f'{parent.user.email}/{parent.path}/{file_name}'
    return new_name
