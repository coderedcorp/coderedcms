from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe

from coderedcms.settings import cr_settings


def get_protected_media_link(request, path, render_link=False):
    if render_link:
        return mark_safe("<a href='{0}{1}'>{0}{1}</a>".format(request.build_absolute_uri('/')[:-1], path))
    return "{0}{1}".format(request.build_absolute_uri('/')[:-1], path)

def uri_validator(possible_uri):
    validate = URLValidator()
    try:
        validate(possible_uri)
        return True
    except ValidationError:
        return False

def attempt_protected_media_value_conversion(request, value):
    new_value = value
    try:
        if value.startswith(cr_settings['PROTECTED_MEDIA_URL']):
            new_value = get_protected_media_link(request, value)
    except AttributeError:
        pass
    return new_value
