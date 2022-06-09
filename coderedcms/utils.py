from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe

from coderedcms.settings import crx_settings


def get_protected_media_link(request, path, render_link=False):
    if render_link:
        return mark_safe(
            "<a href='{0}{1}'>{0}{1}</a>".format(
                request.build_absolute_uri('/')[:-1],
                path
            )
        )
    return "{0}{1}".format(request.build_absolute_uri('/')[:-1], path)


def uri_validator(possible_uri):
    validate = URLValidator()
    try:
        validate(possible_uri)
        return True
    except ValidationError:
        return False


def attempt_protected_media_value_conversion(request, value):
    try:
        if value.startswith(crx_settings.CRX_PROTECTED_MEDIA_URL):
            new_value = get_protected_media_link(request, value)
            return new_value
    except AttributeError:
        pass

    return value


def fix_ical_datetime_format(dt_str):
    """
    ICAL generation gives timezones in the format of 2018-06-30T14:00:00-04:00.
    The Timezone offset -04:00 has a character not recognized by the timezone offset
    code (%z).  The being the colon in -04:00.  We need it to instead be -0400
    """
    if dt_str and ":" == dt_str[-3:-2]:
        dt_str = dt_str[:-3] + dt_str[-2:]
        return dt_str
    return dt_str
