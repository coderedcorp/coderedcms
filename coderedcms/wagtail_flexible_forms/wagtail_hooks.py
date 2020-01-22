from django.conf.urls import url
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.utils import quote
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.helpers import (
    PermissionHelper, PagePermissionHelper, PageAdminURLHelper, AdminURLHelper,
    ButtonHelper)
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import IndexView, InstanceSpecificView
from wagtail.admin import messages
from wagtail.core import hooks
from wagtail.core.models import Page
from wagtail.contrib.forms.utils import get_forms_for_user

from .models import SessionFormSubmission


class FormIndexView(IndexView):
    page_title = _('Forms')


class FormPermissionHelper(PagePermissionHelper):
    def user_can_list(self, user):
        return get_forms_for_user(user).exists()

    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return False

    def user_can_delete_obj(self, user, obj):
        return False

    def user_can_publish_obj(self, user, obj):
        return False

    def user_can_unpublish_obj(self, user, obj):
        return False

    def user_can_copy_obj(self, user, obj):
        return False

    def user_can_inspect_obj(self, user, obj):
        return False


class FormURLHelper(PageAdminURLHelper):
    def _get_action_url_pattern(self, action):
        if action == 'index':
            return r'^stream_forms/$'
        return r'^stream_forms/%s/$' % action


class FormAdmin(ModelAdmin):
    model = Page
    menu_label = _('Forms')
    menu_icon = 'form'
    list_display = ('title', 'unprocessed_submissions_link',
                    'all_submissions_link', 'edit_link')
    index_view_class = FormIndexView
    permission_helper_class = FormPermissionHelper
    url_helper_class = FormURLHelper

    def get_queryset(self, request):
        return get_forms_for_user(request.user)

    def all_submissions_link(self, obj, label=_('See all submissions'),
                             url_suffix=''):
        return '<a href="%s?page_id=%s%s">%s</a>' % (
            reverse(SubmissionAdmin().url_helper.get_action_url_name('index')),
            obj.pk, url_suffix, label)
    all_submissions_link.short_description = ''
    all_submissions_link.allow_tags = True

    def unprocessed_submissions_link(self, obj):
        return self.all_submissions_link(
            obj, _('See unprocessed submissions'),
            '&status=%s' % SubmissionStatusFilter.unprocessed_status)
    unprocessed_submissions_link.short_description = ''
    unprocessed_submissions_link.allow_tags = True

    def edit_link(self, obj):
        return '<a href="%s">%s</a>' % (
            reverse('wagtailadmin_pages:edit', args=(obj.pk,)),
            _('Edit this form page'))
    edit_link.short_description = ''
    edit_link.allow_tags = True


class SubmissionStatusFilter(SimpleListFilter):
    title = _('status')
    parameter_name = 'status'
    unprocessed_status = ','.join((SessionFormSubmission.COMPLETE,
                                   SessionFormSubmission.REVIEWED))

    def lookups(self, request, model_admin):
        yield (self.unprocessed_status, _('Complete or reviewed'))
        for status, verbose_status in SessionFormSubmission.STATUSES:
            if status != SessionFormSubmission.INCOMPLETE:
                yield status, verbose_status

    def queryset(self, request, queryset):
        status = self.value()
        if not status:
            return queryset
        if ',' in status:
            return queryset.filter(status__in=status.split(','))
        return queryset.filter(status=status)


class SubmissionPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return get_forms_for_user(user).exists()

    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return False

    def user_can_inspect_obj(self, user, obj):
        return False

    def user_can_set_status_obj(self, user, obj):
        return user.can_set_status()


class SubmissionURLHelper(AdminURLHelper):
    def _get_action_url_pattern(self, action):
        if action == 'index':
            return r'^%s/%s/$' % (self.opts.app_label, 'submissions')
        return r'^%s/%s/%s/$' % (self.opts.app_label, 'submissions', action)

    def _get_object_specific_action_url_pattern(self, action):
        return r'^%s/%s/%s/(?P<instance_pk>[-\w]+)/$' % (
            self.opts.app_label, 'submissions', action)


class SubmissionButtonHelper(ButtonHelper):
    def set_status_button(self, pk, status, label, title, classnames_add=None,
                          classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.finalise_classname(classnames_add,
                                             classnames_exclude)
        url = self.url_helper.get_action_url('set_status', quote(pk))
        url += '?status=' + status
        return {
            'url': url,
            'label': label,
            'classname': classnames,
            'title': title,
        }

    def reviewed_button(self, pk, classnames_add=None,
                        classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        return self.set_status_button(pk, self.model.REVIEWED,
                                      _('mark as reviewed'),
                                      _('Mark this submission as reviewed'),
                                      classnames_add=classnames_add,
                                      classnames_exclude=classnames_exclude)

    def approve_button(self, pk, classnames_add=None,
                       classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if 'button-secondary' in classnames_add:
            classnames_add.remove('button-secondary')
        classnames_add = ['yes'] + classnames_add
        return self.set_status_button(pk, self.model.APPROVED, _('approve'),
                                      _('Approve this submission'),
                                      classnames_add=classnames_add,
                                      classnames_exclude=classnames_exclude)

    def reject_button(self, pk, classnames_add=None,
                      classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if 'button-secondary' in classnames_add:
            classnames_add.remove('button-secondary')
        classnames_add = ['no'] + classnames_add
        return self.set_status_button(pk, self.model.REJECTED, _('reject'),
                                      _('Reject this submission'),
                                      classnames_add=classnames_add,
                                      classnames_exclude=classnames_exclude)

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None,
                            classnames_exclude=None):
        buttons = super().get_buttons_for_obj(
            obj, exclude=exclude, classnames_add=classnames_add,
            classnames_exclude=classnames_exclude)
        pk = getattr(obj, self.opts.pk.attname)
        status_buttons = []
        if obj.status != obj.REVIEWED:
            status_buttons.append(self.reviewed_button(
                pk, classnames_add=classnames_add,
                classnames_exclude=classnames_exclude))
        if obj.status != obj.APPROVED:
            status_buttons.append(self.approve_button(
                pk, classnames_add=classnames_add,
                classnames_exclude=classnames_exclude))
        if obj.status != obj.REJECTED:
            status_buttons.append(self.reject_button(
                pk, classnames_add=classnames_add,
                classnames_exclude=classnames_exclude))
        return status_buttons + buttons


class SetStatusView(InstanceSpecificView):
    def check_action_permitted(self, user):
        return self.permission_helper.user_can_set_status_obj(user,
                                                              self.instance)

    def get(self, request, *args, **kwargs):
        status = request.GET.get('status')
        if status in dict(self.model.STATUSES):
            previous_status = self.instance.status
            self.instance.status = status
            self.instance.save()
            verbose_label = self.instance.get_status_display()
            if 'revert' in request.GET:
                messages.success(request, 'Reverted to the “%s” status.'
                                 % verbose_label)
            else:
                revert_url = (self.url_helper.get_action_url('set_status',
                                                             self.instance_pk)
                              + '?revert&status=' + previous_status)
                messages.success(
                    request,
                    'Successfully changed the status to “%s”.' % verbose_label,
                    buttons=[messages.button(revert_url, _('Revert'))])
        url = request.META.get('HTTP_REFERER')
        if url is None:
            url = (self.url_helper.get_action_url('index')
                   + '?page_id=%s' % self.instance.page_id)
        return redirect(url)


class SubmissionAdmin(ModelAdmin):
    model = SessionFormSubmission
    menu_icon = 'form'
    permission_helper_class = SubmissionPermissionHelper
    url_helper_class = SubmissionURLHelper
    button_helper_class = SubmissionButtonHelper
    set_status_view_class = SetStatusView
    list_display = ('status', 'user', 'submit_time', 'last_modification')
    list_filter = (SubmissionStatusFilter, 'submit_time', 'last_modification')
    search_fields = ('user__first_name', 'user__last_name')

    def register_with_wagtail(self):
        @hooks.register('register_permissions')
        def register_permissions():
            return self.get_permissions_for_registration()

        @hooks.register('register_admin_urls')
        def register_admin_urls():
            return self.get_admin_urls_for_registration()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        form_pages = get_forms_for_user(request.user)
        return (qs.filter(page__in=form_pages)
                .exclude(status=self.model.INCOMPLETE))

    def get_form_page(self, request):
        form_pages = get_forms_for_user(request.user)
        try:
            return form_pages.get(pk=int(request.GET['page_id'])).specific
        except (KeyError, TypeError, ValueError, Page.DoesNotExist):
            pass

    # TODO: Find a cleaner way to display data from dynamic fields.
    def add_data_bridge(self, name, label):
        def data_bridge(obj):
            return obj.get_data().get(name)

        data_bridge.short_description = label
        setattr(self, name, data_bridge)

    def get_list_display(self, request):
        form_page = self.get_form_page(request)
        if form_page is None:
            return self.list_display
        fields = []
        for name, label in form_page.get_data_fields():
            fields.append(name)
            self.add_data_bridge(name, label)
        return fields

    def set_status_view(self, request, instance_pk):
        kwargs = {'model_admin': self, 'instance_pk': instance_pk}
        view_class = self.set_status_view_class
        return view_class.as_view(**kwargs)(request)

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            url(self.url_helper.get_action_url_pattern('set_status'),
                self.set_status_view,
                name=self.url_helper.get_action_url_name('set_status')),
        )
        return urls


# @hooks.register('construct_main_menu')
# def hide_old_forms_module(request, menu_items):
#     from wagtail.contrib.forms.wagtail_hooks import FormsMenuItem
#     for menu_item in menu_items:
#         if isinstance(menu_item, FormsMenuItem):
#             menu_items.remove(menu_item)

# modeladmin_register(FormAdmin)
# modeladmin_register(SubmissionAdmin)
