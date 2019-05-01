import mimetypes

from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http.response import HttpResponse
from django.utils.html import format_html
from wagtail.contrib.forms.models import AbstractForm
from wagtail.core import hooks
from wagtail.core.models import UserPagePermissionsProxy, get_page_models
from wagtailcache.cache import clear_cache

from coderedcms import utils
from coderedcms.models import CoderedFormPage, CoderedAdvancedFormPage, CoderedFormMixin


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
def clear_wagtailcache(request, page):
    if page.live:
        clear_cache()


@hooks.register('filter_form_submissions_for_user')
def codered_forms(user, editable_forms):
    """
    Add our own CoderedFormPage to editable_forms, since wagtail is unaware
    of its existance. Essentailly this is a fork of wagtail.contrib.forms.get_forms_for_user()
    and wagtail.contrib.forms.get_form_types()
    """
    form_models = [
        model for model in get_page_models()
        if issubclass(model, CoderedFormMixin)
        #if issubclass(model, (AbstractForm, CoderedFormPage))
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
    This hook prevents documents from being downloaded unless specified by an <a> tag with the download attribute.
    """
    content_type, content_encoding = mimetypes.guess_type(document.filename)
    response = HttpResponse(document.file.read(), content_type=content_type)
    response['Content-Disposition'] = 'inline;filename="{0}"'.format(document.filename)
    response['Content-Encoding'] = content_encoding
    return response


from coderedcms.wagtail_flexible_forms.wagtail_hooks import FormAdmin, SubmissionAdmin
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

class CoderedFormAdmin(FormAdmin):
    list_display = ('title', 'action_links')

    def action_links(self, obj):
        actions = []
        if issubclass(type(obj.specific), CoderedFormPage):
            actions.append(
                '<a href="{0}">{1}</a>'.format(reverse('wagtailforms:list_submissions', args=(obj.pk,)), _('See all Submissions'))
            )
            actions.append(
                '<a href="{0}">{1}</a>'.format(reverse('wagtailadmin_pages:edit', args=(obj.pk,)), _('Edit this form page'))
            )
        elif issubclass(type(obj.specific), CoderedAdvancedFormPage):
            actions.append(self.unprocessed_submissions_link(obj))
            actions.append(self.all_submissions_link(obj))
            actions.append(self.edit_link(obj))

        return mark_safe("<br />".join(actions))


class CoderedSubmissionAdmin(SubmissionAdmin):
    pass

from wagtail.contrib.modeladmin.options import modeladmin_register

modeladmin_register(CoderedFormAdmin)
modeladmin_register(CoderedSubmissionAdmin)