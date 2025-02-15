from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.models import get_page_models
from wagtail.permissions import page_permission_policy
from wagtailcache.cache import clear_cache

from coderedcms import __version__


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" type="text/css" href="{}?v={}">',
        static("coderedcms/css/crx-admin.css"),
        __version__,
    )


@hooks.register("insert_editor_js")
def collapsible_js():
    return format_html(
        '<script src="{}?v={}"></script>',
        static("coderedcms/js/crx-editor.js"),
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
hooks.register("after_delete_page", clear_wagtailcache)
hooks.register("after_move_page", clear_wagtailcache)
hooks.register("after_publish_page", clear_wagtailcache)
hooks.register("after_unpublish_page", clear_wagtailcache)
hooks.register("after_create_snippet", clear_wagtailcache)
hooks.register("after_edit_snippet", clear_wagtailcache)
hooks.register("after_delete_snippet", clear_wagtailcache)


@hooks.register("filter_form_submissions_for_user")
def crx_forms(user, editable_forms):
    """
    Add our own CoderedFormPage to editable_forms, since wagtail is unaware
    of its existence. Essentially this is a fork of wagtail.contrib.forms.get_forms_for_user()
    and wagtail.contrib.forms.get_form_types()
    """

    from coderedcms.models import CoderedFormMixin

    # Get content types of pages that inherit from CRX mixins.
    form_models = [
        model
        for model in get_page_models()
        if issubclass(model, (CoderedFormMixin,))
    ]
    form_types = list(ContentType.objects.get_for_models(*form_models).values())

    # Get all pages this user can access.
    all_editable_pages = (
        page_permission_policy.instances_user_has_permission_for(user, "change")
    )
    crx_editable_forms = all_editable_pages.filter(content_type__in=form_types)

    # Combine the previous hook's ``editable_forms`` with our ``editable_forms``.
    combined_forms_pks = list(
        crx_editable_forms.values_list("pk", flat=True)
    ) + list(editable_forms.values_list("pk", flat=True))
    combined_editable_forms = all_editable_pages.filter(
        pk__in=combined_forms_pks
    )

    return combined_editable_forms


class ImportExportMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.is_superuser


@hooks.register("register_settings_menu_item")
def register_import_export_menu_item():
    return ImportExportMenuItem(
        _("Import"),
        reverse("import_index"),
        classnames="icon icon-download",
    )
