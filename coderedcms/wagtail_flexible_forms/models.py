from collections import OrderedDict
from importlib import import_module
from itertools import zip_longest
import json
import os
from pathlib import Path

from PIL import Image
import datetime
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import default_storage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import (
    CharField, TextField, DateTimeField, Model, ForeignKey, PROTECT, CASCADE,
    QuerySet,
)
from django.db.models.fields.files import FieldFile
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.forms import Form, ImageField, FileField, URLField, EmailField
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.safestring import SafeData, mark_safe
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from wagtail.core.models import Page
from wagtail.contrib.forms.models import (
    AbstractForm, AbstractEmailForm, AbstractFormSubmission)

from .blocks import FormStepBlock, FormFieldBlock


class Step:
    def __init__(self, steps, index, struct_child):
        self.steps = steps
        self.index = index
        block = getattr(struct_child, 'block', None)
        if block is None:
            struct_child = []
        if isinstance(block, FormStepBlock):
            self.name = struct_child.value['name']
            self.form_fields = struct_child.value['form_fields']
        else:
            self.name = ''
            self.form_fields = struct_child

    @property
    def index1(self):
        return self.index + 1

    @property
    def url(self):
        return '%s?step=%s' % (self.steps.page.url, self.index1)

    def get_form_fields(self):
        form_fields = OrderedDict()
        field_blocks = self.form_fields
        for struct_child in field_blocks:
            block = struct_child.block
            if isinstance(block, FormFieldBlock):
                struct_value = struct_child.value
                field_name = block.get_slug(struct_value)
                form_fields[field_name] = block.get_field(struct_value)
        return form_fields

    def get_form_class(self):
        return type('WagtailForm', self.steps.page.get_form_class_bases(),
                    self.get_form_fields())

    def get_markups_and_bound_fields(self, form):
        for struct_child in self.form_fields:
            block = struct_child.block
            if isinstance(block, FormFieldBlock):
                struct_value = struct_child.value
                field_name = block.get_slug(struct_value)
                yield form[field_name], 'field'
            else:
                yield mark_safe(struct_child), 'markup'

    def __str__(self):
        if self.name:
            return self.name
        return _('Step %s') % self.index1

    @property
    def badge(self):
        return (mark_safe('<span class="badge">%s/%s</span>')
                % (self.index1, len(self.steps)))

    def __html__(self):
        return '%s %s' % (self, self.badge)

    @property
    def is_active(self):
        return self.index == self.steps.current_index

    @property
    def is_last(self):
        return self.index1 == len(self.steps)

    @property
    def has_prev(self):
        return self.index > 0

    @property
    def has_next(self):
        return self.index1 < len(self.steps)

    @property
    def prev(self):
        if self.has_prev:
            return self.steps[self.index-1]

    @property
    def next(self):
        if self.has_next:
            return self.steps[self.index+1]

    def get_existing_data(self, raw=False):
        data = self.steps.get_existing_data()[self.index]
        fields = self.get_form_fields()
        if not raw:
            class FakeField:
                storage = self.steps.get_storage()

            for field_name, value in data.items():
                if field_name in fields and isinstance(fields[field_name],
                                                       FileField):
                    data[field_name] = FieldFile(None, FakeField, value)
        return data

    @property
    def is_available(self):
        return self.prev is None or self.prev.get_existing_data(raw=True)


class StreamFormJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        try:
            from phonenumber_field.phonenumber import PhoneNumber
        except ImportError:
            pass
        else:
            if isinstance(o, PhoneNumber):
                return str(o)

        return super().default(o)


class Steps(list):
    def __init__(self, page, request=None):
        self.page = page
        # TODO: Make it possible to change the `form_fields` attribute.
        self.form_fields = page.form_fields
        self.request = request
        has_steps = any(isinstance(struct_child.block, FormStepBlock)
                        for struct_child in self.form_fields)
        if has_steps:
            steps = [Step(self, i, form_field)
                     for i, form_field in enumerate(self.form_fields)]
        else:
            steps = [Step(self, 0, self.form_fields)]
        super().__init__(steps)

    def clamp_index(self, index: int):
        if index < 0:
            index = 0
        if index >= len(self):
            index = len(self) - 1
        while not self[index].is_available:
            index -= 1
        return index

    @property
    def current_index(self):
        return self.request.session.get(self.page.current_step_session_key, 0)

    @property
    def current(self):
        return self[self.current_index]

    @current.setter
    def current(self, new_index: int):
        if not isinstance(new_index, int):
            raise TypeError('Use an integer to set the new current step.')
        self.request.session[self.page.current_step_session_key] = \
            self.clamp_index(new_index)

    def forward(self, increment: int = 1):
        self.current = self.current_index + increment

    def backward(self, increment: int = 1):
        self.current = self.current_index - increment

    def get_submission(self):
        return self.page.get_submission(self.request)

    def get_existing_data(self):
        submission = self.get_submission()
        data = [] if submission is None else json.loads(submission.form_data)
        length_difference = len(self) - len(data)
        if length_difference > 0:
            data.extend([{}] * length_difference)
        return data

    def get_current_form(self):
        request = self.request
        if request.method == 'POST':
            step_value = request.POST.get('step', 'next')
            if step_value == 'prev':
                self.backward()
            else:
                return self.current.get_form_class()(
                    request.POST, request.FILES,
                    initial=self.current.get_existing_data())
        return self.current.get_form_class()(
            initial=self.current.get_existing_data())

    def get_storage(self):
        return self.page.get_storage()

    def save_files(self, form):
        submission = self.get_submission()
        for name, field in form.fields.items():
            if isinstance(field, FileField):
                file = form.cleaned_data[name]
                if file == form.initial.get(name, ''):  # Nothing submitted.
                    form.cleaned_data[name] = file.name
                    continue
                if submission is not None:
                    submission.delete_file(name)
                if not file:  # 'Clear' was checked.
                    form.cleaned_data[name] = ''
                    continue
                directory = self.request.session.session_key
                storage = self.get_storage()
                Path(storage.path(directory)).mkdir(parents=True,
                                                    exist_ok=True)
                path = storage.get_available_name(
                    str(Path(directory) / file.name))
                with storage.open(path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                form.cleaned_data[name] = path

    def update_data(self):
        form = self.get_current_form()
        if form.is_valid():
            form_data = self.get_existing_data()
            self.save_files(form)
            form_data[self.current_index] = form.cleaned_data
            form_data = json.dumps(form_data, cls=StreamFormJSONEncoder)
            is_complete = self.current.is_last
            submission = self.get_submission()
            submission.form_data = form_data
            if not submission.is_complete and is_complete:
                submission.status = submission.COMPLETE
            submission.save()
            if is_complete:
                self.current = 0
            else:
                self.forward()
            return is_complete
        return False


class SessionFormSubmission(AbstractFormSubmission):

    session_key = CharField(max_length=40, null=True, default=None)
    user = ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                      related_name='+', on_delete=PROTECT)
    thumbnails_by_path = TextField(default=json.dumps({}))
    last_modification = DateTimeField(_('last modification'), auto_now=True)
    INCOMPLETE = 'incomplete'
    COMPLETE = 'complete'
    REVIEWED = 'reviewed'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUSES = (
        (INCOMPLETE, _('Not submitted')),
        (COMPLETE, _('In progress')),
        (REVIEWED, _('Under consideration')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
    )
    status = CharField(max_length=10, choices=STATUSES, default=INCOMPLETE)

    class Meta:
        verbose_name = _('form submission')
        verbose_name_plural = _('form submissions')
        unique_together = (('page', 'session_key'),
                           ('page', 'user'))
        abstract = True

    @property
    def is_complete(self):
        return self.status != self.INCOMPLETE

    @property
    def form_page(self):
        return self.page.specific

    def get_session(self):
        return import_module(settings.SESSION_ENGINE).SessionStore(
            session_key=self.session_key)

    def reset_step(self):
        session = self.get_session()
        try:
            del session[self.form_page.current_step_session_key]
        except KeyError:
            pass
        else:
            session.save()

    def get_storage(self):
        return self.form_page.get_storage()

    def get_thumbnail_path(self, path, width=64, height=64):
        if not path:
            return ''
        variant = '%s×%s' % (width, height)
        thumbnails_by_path = json.loads(self.thumbnails_by_path)
        thumbnails_paths = thumbnails_by_path.get(path)
        if thumbnails_paths is None:
            thumbnails_by_path[path] = {}
        else:
            thumbnail_path = thumbnails_paths.get(variant)
            if thumbnail_path is not None:
                return thumbnail_path

        path = Path(path)
        thumbnail_path = str(path.with_suffix('.%s%s'
                                              % (variant, path.suffix)))
        storage = self.get_storage()
        thumbnail_path = storage.get_available_name(thumbnail_path)

        thumbnail = Image.open(storage.path(path))
        thumbnail.thumbnail((width, height))
        thumbnail.save(storage.path(thumbnail_path))

        thumbnails_by_path[str(path)][variant] = thumbnail_path
        self.thumbnails_by_path = json.dumps(thumbnails_by_path,
                                             cls=StreamFormJSONEncoder)
        self.save()
        return thumbnail_path

    def get_fields(self, by_step=False):
        return self.form_page.get_form_fields(by_step=by_step)

    def get_existing_thumbnails(self, path):
        thumbnails_paths = json.loads(self.thumbnails_by_path).get(path, {})
        for thumbnail_path in thumbnails_paths.values():
            yield thumbnail_path

    def get_files_by_field(self):
        data = self.get_data(raw=True)
        files = {}
        for name, field in self.get_fields().items():
            if isinstance(field, FileField):
                path = data.get(name)
                if path:
                    files[name] = [path] + list(
                        self.get_existing_thumbnails(path))
        return files

    def get_all_files(self):
        for paths in self.get_files_by_field().values():
            for path in paths:
                yield path

    def delete_file(self, field_name):
        thumbnails_by_path = json.loads(self.thumbnails_by_path)
        for path in self.get_files_by_field().get(field_name, ()):
            self.get_storage().delete(path)
            if path in thumbnails_by_path:
                del thumbnails_by_path[path]
        self.thumbnails_by_path = json.dumps(thumbnails_by_path,
                                             cls=StreamFormJSONEncoder)
        self.save()

    def render_email(self, value):
        return (mark_safe('<a href="mailto:%s" target="_blank">%s</a>')
                % (value, value))

    def render_link(self, value):
        return (mark_safe('<a href="%s" target="_blank">%s</a>')
                % (value, value))

    def render_image(self, value):
        storage = self.get_storage()
        return (mark_safe('<a href="%s" target="_blank"><img src="%s" /></a>')
                % (storage.url(value),
                   storage.url(self.get_thumbnail_path(value))))

    def render_file(self, value):
        return mark_safe('<a href="%s" target="_blank">%s</a>') % (
            self.get_storage().url(value),
            Path(value).name
        )

    def format_value(self, field, value):
        if value is None or value == '':
            return '-'
        new_value = self.form_page.format_value(field, value)
        if new_value != value:
            return new_value
        if value is True:
            return 'Yes'
        if value is False:
            return 'No'
        if isinstance(value, (list, tuple)):
            return ', '.join([self.format_value(field, item)
                              for item in value])
        if isinstance(value, datetime.date):
            return value
        if isinstance(field, EmailField):
            return self.render_email(value)
        if isinstance(field, URLField):
            return self.render_link(value)
        if isinstance(field, ImageField):
            return self.render_image(value)
        if isinstance(field, FileField):
            return self.render_file(value)
        if isinstance(value, SafeData) or hasattr(value, '__html__'):
            return value
        return str(value)

    def format_db_field(self, field_name, raw=False):
        method = getattr(self, 'get_%s_display' % field_name, None)
        if method is not None:
            return method()
        value = getattr(self, field_name)
        if raw:
            return value
        return self.format_value(self._meta.get_field(field_name).formfield(),
                                 value)

    def get_steps_data(self, raw=False):
        steps_data = json.loads(self.form_data)
        if raw:
            return steps_data
        fields_and_data_iterator = zip_longest(self.get_fields(by_step=True),
                                               steps_data, fillvalue={})
        return [
            OrderedDict([(name, self.format_value(field, step_data.get(name)))
                         for name, field in step_fields.items()])
            for step_fields, step_data in fields_and_data_iterator]

    def get_extra_data(self, raw=False):
        return self.form_page.get_extra_data(self, raw=raw)

    def get_data(self, raw=False, add_metadata=True):
        steps_data = self.get_steps_data(raw=raw)
        form_data = {}
        form_data.update(self.get_extra_data(raw=raw))
        for step_data in steps_data:
            form_data.update(step_data)
        if add_metadata:
            form_data.update(
                status=self.format_db_field('status', raw=raw),
                user=self.format_db_field('user', raw=raw),
                submit_time=self.format_db_field('submit_time', raw=raw),
                last_modification=self.format_db_field('last_modification',
                                                       raw=raw),
            )
        return form_data

    def steps_with_data_iterator(self, raw=False):
        for step, step_data_fields, step_data in zip(
                self.form_page.get_steps(),
                self.form_page.get_data_fields(by_step=True),
                self.get_steps_data(raw=raw)):
            yield step, [(field_name, field_label, step_data[field_name])
                         for field_name, field_label in step_data_fields]


@receiver(post_delete, sender=SessionFormSubmission)
def delete_files(sender, **kwargs):
    instance = kwargs['instance']
    instance.reset_step()
    storage = instance.get_storage()
    for path in instance.get_all_files():
        storage.delete(path)

        # Automatically deletes ancestor folders if empty.
        directory = Path(path)
        while directory.parent != Path(directory.root):
            directory = directory.parent
            try:
                subdirectories, files = storage.listdir(directory)
            except FileNotFoundError:
                continue
            if not subdirectories and not files:
                Path(storage.path(directory)).rmdir()


class SubmissionRevisionQuerySet(QuerySet):
    def for_submission(self, submission):
        return self.filter(**self.model.get_filters_for(submission))

    def created(self):
        return self.filter(type=self.model.CREATED)

    def changed(self):
        return self.filter(type=self.model.CHANGED)

    def deleted(self):
        return self.filter(type=self.model.DELETED)


class SubmissionRevision(Model):
    CREATED = 'created'
    CHANGED = 'changed'
    DELETED = 'deleted'
    TYPES = (
        (CREATED, _('Created')),
        (CHANGED, _('Changed')),
        (DELETED, _('Deleted')),
    )
    type = CharField(max_length=7, choices=TYPES)
    created_at = DateTimeField(auto_now_add=True)
    submission_ct = ForeignKey('contenttypes.ContentType', on_delete=CASCADE)
    submission_id = TextField()
    submission = GenericForeignKey('submission_ct', 'submission_id')
    data = TextField()
    summary = TextField()

    objects = SubmissionRevisionQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)
        abstract = True

    @staticmethod
    def get_filters_for(submission):
        return {
            'submission_ct':
                ContentType.objects.get_for_model(submission._meta.model),
            'submission_id': str(submission.pk),
        }

    @classmethod
    def diff_summary(cls, page, data1, data2):
        diff = []
        data_fields = page.get_data_fields()
        hidden_types = (tuple, list, dict)
        for k, label in data_fields:
            value1 = data1.get(k)
            value2 = data2.get(k)
            if value2 == value1 or not value1 and not value2:
                continue
            is_hidden = (isinstance(value1, hidden_types)
                         or isinstance(value2, hidden_types))

            # Escapes newlines as they are used as separator inside summaries.
            if isinstance(value1, str):
                value1 = value1.replace('\n', r'\n')
            if isinstance(value2, str):
                value2 = value2.replace('\n', r'\n')

            if value2 and not value1:
                diff.append(
                    ((_('“%s” set.') % label) if is_hidden
                     else (_('“%s” set to “%s”.')) % (label, value2)))
            elif value1 and not value2:
                diff.append(_('“%s” unset.') % label)
            else:
                diff.append(((_('“%s” changed.') % label) if is_hidden
                             else (_('“%s” changed from “%s” to “%s”.')
                                   % (label, value1, value2))))
        return '\n'.join(diff)

    @classmethod
    def create_from_submission(cls, submission, revision_type):
        page = submission.form_page
        try:
            previous = cls.objects.for_submission(
                submission).latest('created_at')
        except cls.DoesNotExist:
            previous_data = {}
        else:
            previous_data = previous.get_data()
        filters = cls.get_filters_for(submission)
        data = submission.get_data(raw=True, add_metadata=False)
        data['status'] = submission.status
        if revision_type == cls.CREATED:
            summary = _('Submission created.')
        elif revision_type == cls.DELETED:
            summary = _('Submission deleted.')
        else:
            summary = cls.diff_summary(page, previous_data, data)
        if not summary:  # Nothing changed.
            return
        filters.update(
            type=revision_type, data=json.dumps(data, cls=StreamFormJSONEncoder), summary=summary
        )
        return cls.objects.create(**filters)

    def get_data(self):
        return json.loads(self.data)

# ORIGINAL NORIPYT CODE.
# We don't want these receivers triggering.

# @receiver(post_save)
# def create_submission_changed_revision(sender, **kwargs):
#     if not issubclass(sender, SessionFormSubmission):
#         return
#     submission = kwargs['instance']
#     created = kwargs['created']
#     SubmissionRevision.create_from_submission(
#         submission, (SubmissionRevision.CREATED if created
#                      else SubmissionRevision.CHANGED))


# @receiver(post_delete)
# def create_submission_deleted_revision(sender, **kwargs):
#     if not issubclass(sender, SessionFormSubmission):
#         return
#     submission = kwargs['instance']
#     SubmissionRevision.create_from_submission(submission,
#                                               SubmissionRevision.DELETED)


class StreamFormMixin:
    preview_modes = Page.DEFAULT_PREVIEW_MODES

    @property
    def current_step_session_key(self):
        return '%s:step' % self.pk

    def get_steps(self, request=None):
        if not hasattr(self, 'steps'):
            steps = Steps(self, request=request)
            if request is None:
                return steps
            self.steps = steps
        return self.steps

    def get_form_fields(self, by_step=False):
        if by_step:
            return [step.get_form_fields() for step in self.get_steps()]
        form_fields = OrderedDict()
        for step_fields in self.get_form_fields(by_step=True):
            form_fields.update(step_fields)
        return form_fields

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        self.steps = self.get_steps(request)
        step_value = request.GET.get('step')
        if step_value is not None and step_value.isdigit():
            self.steps.current = int(step_value) - 1
        form = self.steps.get_current_form()
        context.update(
            steps=self.steps,
            step=self.steps.current,
            form=form,
            markups_and_bound_fields=list(
                self.steps.current.get_markups_and_bound_fields(form)),
        )
        return context

    def get_storage(self):
        return default_storage

    @staticmethod
    def get_form_class_bases():
        return Form,

    @staticmethod
    def get_submission_class():
        return SessionFormSubmission

    def get_submission(self, request):
        Submission = self.get_submission_class()
        if request.user.is_authenticated:
            user_submission = Submission.objects.filter(
                user=request.user, page=self).order_by('-pk').first()
            if user_submission is None:
                return Submission(user=request.user, page=self, form_data='[]')
            return user_submission

        user_submission = Submission.objects.filter(
            session_key=request.session.session_key, page=self
        ).order_by('-pk').first()
        if user_submission is None:
            return Submission(session_key=request.session.session_key,
                              page=self, form_data='[]')
        return user_submission

    def get_success_url(self):
        form_complete_models = [model for model in apps.get_models()
                                if issubclass(model, FormCompleteMixin)]
        cts = (ContentType.objects
               .get_for_models(*form_complete_models).values())
        first_child = self.get_children().filter(content_type__in=cts).first()
        if first_child is None:
            return self.url
        return first_child.url

    def serve_success(self, request, *args, **kwargs):
        url = self.get_success_url()
        if url == self.url:
            messages.success(request,
                             _('Successfully submitted the form.'))
        return HttpResponseRedirect(url)

    def serve(self, request, *args, **kwargs):
        context = self.get_context(request)
        form = context['form']
        if request.method == 'POST' and form.is_valid():
            is_complete = self.steps.update_data()
            if is_complete:
                return self.serve_success(request, *args, **kwargs)
            return HttpResponseRedirect(self.url)
        return Page.serve(self, request, *args, **kwargs)

    def get_data_fields(self, by_step=False, add_metadata=True):
        if by_step:
            return [[(field_name, field.label)
                     for field_name, field in step_fields.items()]
                    for step_fields in self.get_form_fields(by_step=True)]

        data_fields = []
        data_fields.extend(self.get_extra_data_fields())
        if add_metadata:
            data_fields.extend((
                ('status', _('Status')),
                ('user', _('User')),
                ('submit_time', _('First modification')),
                ('last_modification', _('Last modification'))))
        data_fields.extend([
            (field_name, field_label)
            for step_data_fields in self.get_data_fields(by_step=True)
            for field_name, field_label in step_data_fields])
        return data_fields

    def get_extra_data_fields(self):
        return ()

    def get_extra_data(self, submission, raw=False):
        return {}

    def format_value(self, field, value):
        return value


class ClosingFormMixin(Model):
    closing_at = DateTimeField()

    closed_template = None

    class Meta:
        abstract = True

    @property
    def is_closed(self):
        return now() > self.closing_at

    def get_closed_template(self, request, *args, **kwargs):
        if self.closed_template is None:
            template = self.get_template(request, *args, **kwargs)
            base, ext = os.path.splitext(template)
            return '%s_closed%s' % (base, ext)
        return self.closed_template

    def serve_closed(self, request, *args, **kwargs):
        return TemplateResponse(
            request,
            self.get_closed_template(request, *args, **kwargs),
            self.get_context(request, *args, **kwargs),
        )

    def serve(self, request, *args, **kwargs):
        if self.is_closed:
            return self.serve_closed(request, *args, **kwargs)
        return super().serve(request, *args, **kwargs)


class FormCompleteMixin:
    def get_form_page(self):
        return self.get_parent().specific

    def serve(self, request, *args, **kwargs):
        form_page = self.get_form_page()
        if isinstance(form_page, LoginRequiredMixin) \
                and not request.user.is_authenticated():
            return HttpResponseRedirect(form_page.url)
        self.submission = form_page.get_submission(request)
        if self.submission is not None and self.submission.is_complete \
                or getattr(request, 'is_preview', False):
            return super().serve(request, *args, **kwargs)
        return HttpResponseRedirect(form_page.url)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        if hasattr(self, 'submission'):
            context['submission'] = self.submission
        return context


class LoginRequiredMixin:
    login_required_template = None

    def get_login_required_template(self, request, *args, **kwargs):
        if self.login_required_template is None:
            template = self.get_template(request, *args, **kwargs)
            base, ext = os.path.splitext(template)
            return '%s_login_required%s' % (base, ext)
        return self.login_required_template

    def serve_login_required(self, request, *args, **kwargs):
        return TemplateResponse(
            request,
            self.get_login_required_template(request, *args, **kwargs),
            self.get_context(request, *args, **kwargs),
        )

    def serve(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return self.serve_login_required(request, *args, **kwargs)
        return super().serve(request, *args, **kwargs)


class AbstractStreamForm(StreamFormMixin, AbstractForm):
    class Meta:
        abstract = True


class AbstractEmailStreamForm(StreamFormMixin, AbstractEmailForm):
    class Meta:
        abstract = True
