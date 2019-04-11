import string
import random
from datetime import datetime
from django import template
from django.conf import settings
from django.forms import ClearableFileInput
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.formats import localize
from wagtail.core.models import Collection
from wagtail.core.rich_text import RichText
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images.models import Image

from coderedcms import utils, __version__
from coderedcms.blocks import CoderedAdvSettings
from coderedcms.forms import SearchForm
from coderedcms.models import Footer, Navbar
from coderedcms.settings import cr_settings, get_bootstrap_setting

register = template.Library()

@register.filter
def get_embed_video_provider(url):
    if 'youtu.be' in url or 'youtube.com' in url:
        return 'youtube'
    if 'vimeo.com' in url:
        return 'vimeo'
    return ''

@register.filter
def get_embed_video_code(url):
    if get_embed_video_provider(url) == 'youtube':
        v = url.split('v=', 1)[1]
        return v.split('&', 1)[0]
    if get_embed_video_provider(url) == 'vimeo':
        v = url.split('.com/', 1)[1]
        return v.split('?', 1)[0]
    return ''

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
    return ''.join(random.choice(string.ascii_letters + string.digits) for n in range(20))

@register.simple_tag
def is_menu_item_dropdown(value):
    return \
        len(value.get('sub_links', [])) > 0 or \
        (
            value.get('show_child_links', False) and \
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
def process_form_cell(request, cell):
    if isinstance(cell, str) and cell.startswith(cr_settings['PROTECTED_MEDIA_URL']):
        return utils.get_protected_media_link(request, cell, render_link=True)
    if utils.uri_validator(str(cell)):
        return mark_safe("<a href='{0}'>{1}</a>".format(cell, cell))
    return localize(cell)

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
            except:
                pass
    return get

@register.filter
def structured_data_datetime(dt):
    """
    Formats datetime object to structured data compatible datetime string.
    """
    if dt.time():
        return datetime.strftime(dt, "%Y-%m-%dT%H:%M")
    return datetime.strftime(dt, "%Y-%m-%d")

@register.filter
def richtext_amp(value):

    if isinstance(value, RichText):
        value = richtext(value.source)
    else:
        value = richtext(value)

    value = utils.convert_to_amp(value)
    return mark_safe(value)
