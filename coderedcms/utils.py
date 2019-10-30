from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe

from coderedcms.settings import cr_settings


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
        if value.startswith(cr_settings['PROTECTED_MEDIA_URL']):
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


def convert_to_amp(value, pretty=True):
    """
    Function that converts non-amp compliant html to valid amp html.
    value must be a string
    """
    soup = BeautifulSoup(value, "html.parser")

    # Replace img tags with amp-img
    try:
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            img_tag.name = 'amp-img'
    except AttributeError:
        pass

    # Replace iframe tags with amp-iframe
    try:
        iframe_tags = soup.find_all('iframe')
        for iframe_tag in iframe_tags:
            iframe_tag.name = 'amp-iframe'
            iframe_tag['layout'] = 'responsive'

    except AttributeError:
        pass

    if pretty:
        return soup.prettify()

    return str(soup)


def process_richtext(value, request=None, pretty=True):
    if not request:
        return value

    from coderedcms.models.wagtailsettings_models import LayoutSettings

    soup = BeautifulSoup(value, "html.parser")
    layout_settings = LayoutSettings.for_site(request.site)
    if layout_settings.new_tab:

        try:
            a_tags = soup.find_all('a')
            for a_tag in a_tags:
                a_tag['target'] = '_blank'
        except AttributeError:
            pass

    if pretty:
        return soup.prettify()

    return str(soup)
