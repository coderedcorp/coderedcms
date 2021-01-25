import string
import random
import re

from bs4 import BeautifulSoup
from datetime import datetime
from django import template
from django.conf import settings
from django.forms import ClearableFileInput
from django.utils.html import mark_safe
from wagtail.core.models import Collection, Site
from wagtail.core.rich_text import RichText
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images.models import Image

from coderedcms import utils, __version__
from coderedcms.blocks import CoderedAdvSettings
from coderedcms.forms import SearchForm
from coderedcms.models import Footer, Navbar
from coderedcms.settings import cr_settings, get_bootstrap_setting
from coderedcms.models.wagtailsettings_models import LayoutSettings

register = template.Library()


@register.filter
def is_advanced_setting(obj):
    return CoderedAdvSettings in (obj.__class__,) + obj.__class__.__bases__


@register.filter
def is_file_form(form):
    return any([isinstance(field.field.widget, ClearableFileInput) for field in form])


@register.simple_tag
def coderedcms_version():
    return __version__


@register.simple_tag
def generate_random_id():
    value = ''.join(random.choice(string.ascii_letters + string.digits) for n in range(20))
    return "cr-{}".format(value)


@register.simple_tag(takes_context=True)
def og_image(context, page):

    # Fixes #240 https://github.com/coderedcorp/coderedcms/issues/240
    # Prepend the site's root URL except for when MEDIA_URL already
    # looks like a full URL.
    protocol = re.compile(r'^(\w[\w\.\-\+]*:)*//')

    if protocol.match(settings.MEDIA_URL):
        base_url = ''
    else:
        base_url = Site.find_for_request(context['request']).root_url

    if page:
        if page.og_image:
            return base_url + page.og_image.get_rendition('original').url
        elif page.cover_image:
            return base_url + page.cover_image.get_rendition('original').url

    layout_settings = LayoutSettings.for_request(context['request'])
    if layout_settings.logo:
        return base_url + layout_settings.logo.get_rendition('original').url

    return None


@register.simple_tag
def is_menu_item_dropdown(value):
    return \
        len(value.get('sub_links', [])) > 0 or \
        (
            value.get('show_child_links', False) and
            len(value.get('page', []).get_children().live()) > 0
        )


@register.simple_tag(takes_context=True)
def is_active_page(context, curr_page, other_page):
    if hasattr(curr_page, 'get_url') and hasattr(other_page, 'get_url'):
        curr_url = curr_page.get_url(context['request'])
        other_url = other_page.get_url(context['request'])
        return curr_url == other_url
    return False


@register.simple_tag
def get_pictures(collection_id):
    collection = Collection.objects.get(id=collection_id)
    return Image.objects.filter(collection=collection)


@register.simple_tag(takes_context=True)
def get_navbar_css(context):
    layout = LayoutSettings.for_request(context['request'])
    fixed = "fixed-top" if layout.navbar_fixed else ""
    return " ".join([
        fixed,
        layout.navbar_collapse_mode,
        layout.navbar_color_scheme,
        layout.navbar_format,
        layout.navbar_class
    ])


@register.simple_tag
def get_navbars():
    return Navbar.objects.all()


@register.simple_tag
def get_footers():
    return Footer.objects.all()


@register.simple_tag
def get_searchform(request=None):
    if request:
        return SearchForm(request.GET)
    return SearchForm()


@register.simple_tag
def get_pageform(page, request):
    return page.get_form(request)


@register.simple_tag
def process_form_cell(request, cell):
    if isinstance(cell, str) and cell.startswith(cr_settings['PROTECTED_MEDIA_URL']):
        return utils.get_protected_media_link(request, cell, render_link=True)
    if utils.uri_validator(str(cell)):
        return mark_safe("<a href='{0}'>{1}</a>".format(cell, cell))
    return cell


@register.filter
def codered_settings(value):
    return cr_settings.get(value, None)


@register.filter
def bootstrap_settings(value):
    return get_bootstrap_setting(value)


@register.filter
def django_settings(value):
    return getattr(settings, value)


@register.simple_tag
def query_update(querydict, key=None, value=None):
    """
    Alters querydict (request.GET) by updating/adding/removing key to value
    """
    get = querydict.copy()
    if key:
        if value:
            get[key] = value
        else:
            try:
                del(get[key])
            except KeyError:
                pass
    return get


@register.filter
def structured_data_datetime(dt):
    """
    Formats datetime object to structured data compatible datetime string.
    """
    try:
        if dt.time():
            return datetime.strftime(dt, "%Y-%m-%dT%H:%M")
        return datetime.strftime(dt, "%Y-%m-%d")
    except AttributeError:
        return ""


@register.filter
def convert_to_amp(value):
    """
    Converts HTML to AMP.
    """
    if isinstance(value, RichText):
        value = richtext(value.source)
    return mark_safe(utils.convert_to_amp(value))


@register.simple_tag
def render_iframe_from_embed(embed):
    soup = BeautifulSoup(embed.html, "html.parser")
    try:
        iframe_tags = soup.find('iframe')
        iframe_tags['title'] = embed.title
        return mark_safe(soup.prettify())
    except AttributeError:
        pass
    except TypeError:
        pass

    return mark_safe(embed.html)


@register.filter
def map_to_bootstrap_alert(message_tag):
    """
    Converts a message level to a bootstrap 4 alert class
    """
    message_to_alert_dict = {
        'debug': 'primary',
        'info': 'info',
        'success': 'success',
        'warning': 'warning',
        'error': 'danger'
    }

    try:
        return message_to_alert_dict[message_tag]
    except KeyError:
        return ''
