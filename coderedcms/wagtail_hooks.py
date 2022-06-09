import mimetypes

from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
from django.http.response import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks
from wagtail.core.models import UserPagePermissionsProxy, get_page_models
from wagtailcache.cache import clear_cache

from coderedcms import __version__


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" type="text/css" href="{}?v={}">',
        static('coderedcms/css/codered-admin.css'),
        __version__,
    )


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" type="text/css" href="{}?v={}">',
        static('coderedcms/css/codered-editor.css'),
        __version__,
    )


@hooks.register('insert_editor_js')
def collapsible_js():
    return format_html(
        '<script src="{}?v={}"></script>',
        static('coderedcms/js/codered-editor.js'),
        __version__,
    )


@hooks.register("register_icons")
def register_icons(icons):
    """
    Add custom SVG icons to the Wagtail admin.
    """
    # These SVG files should be in the django templates folder, and follow exact
    # specifications to work with Wagtail:
    # https://github.com/wagtail/wagtail/pull/6028
    icons.append("coderedcms/icons/cr-align-left.svg")
    icons.append("coderedcms/icons/cr-check-square-o.svg")
    icons.append("coderedcms/icons/cr-columns.svg")
    icons.append("coderedcms/icons/cr-desktop.svg")
    icons.append("coderedcms/icons/cr-font.svg")
    icons.append("coderedcms/icons/cr-google.svg")
    icons.append("coderedcms/icons/cr-hand-pointer-o.svg")
    icons.append("coderedcms/icons/cr-hashtag.svg")
    icons.append("coderedcms/icons/cr-header.svg")
    icons.append("coderedcms/icons/cr-list-alt.svg")
    icons.append("coderedcms/icons/cr-map.svg")
    icons.append("coderedcms/icons/cr-newspaper-o.svg")
    icons.append("coderedcms/icons/cr-puzzle-piece.svg")
    icons.append("coderedcms/icons/cr-recycle.svg")
    icons.append("coderedcms/icons/cr-stop.svg")
    icons.append("coderedcms/icons/cr-th-large.svg")
    icons.append("coderedcms/icons/cr-universal-access.svg")
    icons.append("coderedcms/icons/cr-usd.svg")
    icons.append("coderedcms/icons/cr-window-maximize.svg")
    icons.append("coderedcms/icons/cr-window-minimize.svg")
    return icons


def clear_wagtailcache(*args, **kwargs):
    clear_cache()


# Clear cache whenever pages/snippets are changed. Err on the side of clearing
# the cache vs not clearing the cache, as this usually leads to support requests
# when staff members make edits but do not see the changes.
hooks.register('after_delete_page', clear_wagtailcache)
hooks.register('after_move_page', clear_wagtailcache)
hooks.register('after_publish_page', clear_wagtailcache)
hooks.register('after_unpublish_page', clear_wagtailcache)
hooks.register('after_create_snippet', clear_wagtailcache)
hooks.register('after_edit_snippet', clear_wagtailcache)
hooks.register('after_delete_snippet', clear_wagtailcache)


@hooks.register('filter_form_submissions_for_user')
def codered_forms(user, editable_forms):
    """
    Add our own CoderedFormPage to editable_forms, since wagtail is unaware
    of its existence. Essentially this is a fork of wagtail.contrib.forms.get_forms_for_user()
    and wagtail.contrib.forms.get_form_types()
    """
    from coderedcms.models import CoderedFormMixin
    form_models = [
        model for model in get_page_models()
        if issubclass(model, CoderedFormMixin)
    ]
    form_types = list(
        ContentType.objects.get_for_models(*form_models).values()
    )

    editable_forms = UserPagePermissionsProxy(user).editable_pages()
    editable_forms = editable_forms.filter(content_type__in=form_types)

    return editable_forms


@hooks.register('before_serve_document')
def serve_document_directly(document, request):
    """
    This hook prevents documents from being downloaded unless
    specified by an <a> tag with the download attribute.
    """
    content_type, content_encoding = mimetypes.guess_type(document.filename)
    response = HttpResponse(document.file.read(), content_type=content_type)
    response['Content-Disposition'] = 'inline;filename="{0}"'.format(document.filename)
    response['Content-Encoding'] = content_encoding
    return response


class ImportExportMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.is_superuser


@hooks.register('register_settings_menu_item')
def register_import_export_menu_item():
    return ImportExportMenuItem(
        _('Import'),
        reverse('import_index'),
        classnames='icon icon-download',
    )
