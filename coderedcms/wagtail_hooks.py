import mimetypes

from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
from django.http.response import HttpResponse
from django.urls import reverse
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.core import hooks
from wagtail.core.models import UserPagePermissionsProxy, get_page_models
from wagtailcache.cache import clear_cache

from coderedcms.wagtail_flexible_forms.wagtail_hooks import FormAdmin, SubmissionAdmin


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" type="text/css" href="{}">',
        static('coderedcms/css/codered-admin.css')
    )


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" type="text/css" href="{}">',
        static('coderedcms/css/codered-editor.css')
    )


@hooks.register('insert_editor_js')
def collapsible_js():
    return format_html('<script src="{}"></script>', static('coderedcms/js/codered-editor.js'))


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def clear_wagtailcache(request, page):
    if page.live:
        clear_cache()


@hooks.register('filter_form_submissions_for_user')
def codered_forms(user, editable_forms):
    from coderedcms.models import CoderedFormMixin
    """
    Add our own CoderedFormPage to editable_forms, since wagtail is unaware
    of its existence. Essentially this is a fork of wagtail.contrib.forms.get_forms_for_user()
    and wagtail.contrib.forms.get_form_types()
    """
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


class CoderedSubmissionAdmin(SubmissionAdmin):

    def __init__(self, parent=None):
        from coderedcms.models import CoderedSessionFormSubmission
        self.model = CoderedSessionFormSubmission
        super().__init__(parent=parent)


class CoderedFormAdmin(FormAdmin):
    list_display = ('title', 'action_links')

    def all_submissions_link(self, obj, label=_('See all submissions'),
                             url_suffix=''):
        return '<a href="%s?page_id=%s%s">%s</a>' % (
            reverse(CoderedSubmissionAdmin().url_helper.get_action_url_name('index')),
            obj.pk, url_suffix, label)
    all_submissions_link.short_description = ''
    all_submissions_link.allow_tags = True

    def action_links(self, obj):
        from coderedcms.models import CoderedFormPage, CoderedStreamFormPage
        actions = []
        if issubclass(type(obj.specific), CoderedFormPage):
            actions.append(
                '<a href="{0}">{1}</a>'.format(reverse(
                    'wagtailforms:list_submissions',
                    args=(obj.pk,)),
                    _('See all Submissions')
                )
            )
            actions.append(
                '<a href="{0}">{1}</a>'.format(
                    reverse("wagtailadmin_pages:edit", args=(obj.pk,)), _("Edit this form page")
                )
            )
        elif issubclass(type(obj.specific), CoderedStreamFormPage):
            actions.append(self.unprocessed_submissions_link(obj))
            actions.append(self.all_submissions_link(obj))
            actions.append(self.edit_link(obj))

        return mark_safe("<br />".join(actions))

# modeladmin_register(CoderedFormAdmin)
# modeladmin_register(CoderedSubmissionAdmin)
