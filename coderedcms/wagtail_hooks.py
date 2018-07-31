from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from wagtail.contrib.forms.models import AbstractForm
from wagtail.core import hooks
from wagtail.core.models import UserPagePermissionsProxy, get_page_models

from coderedcms import utils
from coderedcms.models import CoderedFormPage


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" type="text/css" href="{}">', static('css/codered-admin.css'))


@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" type="text/css" href="{}">', static('css/codered-editor.css'))


@hooks.register('insert_editor_js')
def collapsible_js():
    return format_html('<script src="{}"></script>', static('js/codered-editor.js'))


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def clear_cache(request, page):
    if page.live:
        utils.clear_cache()


@hooks.register('filter_form_submissions_for_user')
def codered_forms(user, editable_forms):
    """
    Add our own CoderedFormPage to editable_forms, since wagtail is unaware
    of its existance. Essentailly this is a fork of wagtail.contrib.forms.get_forms_for_user()
    and wagtail.contrib.forms.get_form_types()
    """
    form_models = [
        model for model in get_page_models()
        if issubclass(model, (AbstractForm, CoderedFormPage))
    ]
    form_types = list(
        ContentType.objects.get_for_models(*form_models).values()
    )

    editable_forms = UserPagePermissionsProxy(user).editable_pages()
    editable_forms = editable_forms.filter(content_type__in=form_types)

    return editable_forms
