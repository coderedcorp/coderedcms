import string
import random

from bs4 import BeautifulSoup
from django import template
from django.db.models.query import QuerySet
from django.forms import ClearableFileInput
from django.utils.html import mark_safe
from wagtail.core.models import Collection
from wagtail.images.models import Image

from coderedcms import utils, __version__
from coderedcms.blocks import CoderedAdvSettings
from coderedcms.forms import SearchForm
from coderedcms.models.snippet_models import Navbar, Footer
from coderedcms.settings import crx_settings as crx_settings_obj
from coderedcms.settings import get_bootstrap_setting
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


@register.simple_tag(takes_context=True)
def get_navbars(context) -> 'QuerySet[Navbar]':
    layout = LayoutSettings.for_request(context['request'])
    navbarorderables = layout.site_navbar.all()
    navbars = Navbar.objects.filter(
        navbarorderable__in=navbarorderables
        ).order_by('navbarorderable__sort_order')
    return navbars


@register.simple_tag(takes_context=True)
def get_footers(context) -> 'QuerySet[Footer]':
    layout = LayoutSettings.for_request(context['request'])
    footerorderables = layout.site_footer.all()
    footers = Footer.objects.filter(
        footerorderable__in=footerorderables
        ).order_by('footerorderable__sort_order')
    return footers


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
    if isinstance(cell, str) and cell.startswith(crx_settings_obj.CRX_PROTECTED_MEDIA_URL):
        return utils.get_protected_media_link(request, cell, render_link=True)
    if utils.uri_validator(str(cell)):
        return mark_safe("<a href='{0}'>{1}</a>".format(cell, cell))
    return cell


@register.filter
def crx_settings(value):
    return getattr(crx_settings_obj, value)


@register.filter
def bootstrap_settings(value):
    return get_bootstrap_setting(value)


@register.filter
def django_settings(value):
    return getattr(crx_settings_obj, value)


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


@register.filter
def get_name_of_class(class_type):
    if hasattr(class_type.__class__, "search_name"):
        return class_type.__class__.search_name
    elif (
            hasattr(class_type.__class__, "_meta") and
            hasattr(class_type.__class__._meta, "verbose_name")
    ):
        return class_type.__class__._meta.verbose_name
    else:
        return class_type.__class__.__name__


@register.filter
def get_plural_name_of_class(class_type):
    if hasattr(class_type.__class__, "search_name_plural"):
        return class_type.__class__.search_name_plural
    elif (
            hasattr(class_type.__class__, "_meta") and
            hasattr(class_type.__class__._meta, "verbose_name_plural")
    ):
        return class_type.__class__._meta.verbose_name_plural
    else:
        return class_type.__class__.__name__ + "s"
