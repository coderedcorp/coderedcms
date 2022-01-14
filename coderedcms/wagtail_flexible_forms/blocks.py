from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.dateparse import parse_datetime
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from anyascii import anyascii
from wagtail.core.blocks import (
    StructBlock, TextBlock, CharBlock, BooleanBlock, ListBlock, StreamBlock,
    DateBlock, TimeBlock, DateTimeBlock, ChoiceBlock, RichTextBlock,
)


class FormFieldBlock(StructBlock):
    field_label = CharBlock(label=_('Label'))
    help_text = TextBlock(required=False, label=_('Help text'))

    field_class = forms.CharField
    widget = None

    def get_slug(self, struct_value):
        return slugify(anyascii(struct_value['field_label']))

    def get_field_class(self, struct_value):
        return self.field_class

    def get_widget(self, struct_value):
        return self.widget

    def get_field_kwargs(self, struct_value):
        kwargs = {'label': struct_value['field_label'],
                  'help_text': struct_value['help_text'],
                  'required': struct_value.get('required', False)}
        if 'default_value' in struct_value:
            kwargs['initial'] = struct_value['default_value']
        form_widget = self.get_widget(struct_value)
        if form_widget is not None:
            kwargs['widget'] = form_widget
        return kwargs

    def get_field(self, struct_value):
        return self.get_field_class(struct_value)(
            **self.get_field_kwargs(struct_value))


class OptionalFormFieldBlock(FormFieldBlock):
    required = BooleanBlock(label=_('Required'), required=False)


CHARFIELD_FORMATS = [
    ('email', _('Email')),
    ('url', _('URL')),
]
try:
    from phonenumber_field.formfields import PhoneNumberField
except ImportError:
    pass
else:
    CHARFIELD_FORMATS.append(('phone', _('Phone')))


class CharFieldBlock(OptionalFormFieldBlock):
    format = ChoiceBlock(choices=CHARFIELD_FORMATS, required=False, label=_('Format'))
    default_value = CharBlock(required=False, label=_('Default value'))

    class Meta:
        label = _('Text field (single line)')

    def get_field_class(self, struct_value):
        text_format = struct_value['format']
        if text_format == 'url':
            return forms.URLField
        if text_format == 'email':
            return forms.EmailField
        if text_format == 'phone':
            return PhoneNumberField
        return super().get_field_class(struct_value)


class TextFieldBlock(OptionalFormFieldBlock):
    default_value = TextBlock(required=False, label=_('Default value'))

    widget = forms.Textarea(attrs={'rows': 5})

    class Meta:
        label = _('Text field (multi line)')


class NumberFieldBlock(OptionalFormFieldBlock):
    default_value = CharBlock(required=False, label=_('Default value'))

    widget = forms.NumberInput

    class Meta:
        label = _('Number field')


class CheckboxFieldBlock(FormFieldBlock):
    default_value = BooleanBlock(required=False)

    field_class = forms.BooleanField

    class Meta:
        label = _('Checkbox field')
        icon = 'tick-inverse'


class RadioButtonsFieldBlock(OptionalFormFieldBlock):
    choices = ListBlock(CharBlock(label=_('Choice')))

    field_class = forms.ChoiceField
    widget = forms.RadioSelect

    class Meta:
        label = _('Radio buttons')
        icon = 'radio-empty'

    def get_field_kwargs(self, struct_value):
        kwargs = super().get_field_kwargs(struct_value)
        kwargs['choices'] = [(choice, choice)
                             for choice in struct_value['choices']]
        return kwargs


class DropdownFieldBlock(RadioButtonsFieldBlock):
    widget = forms.Select

    class Meta:
        label = _('Dropdown field')
        icon = 'arrow-down-big'

    def get_field_kwargs(self, struct_value):
        kwargs = super(DropdownFieldBlock,
                       self).get_field_kwargs(struct_value)
        kwargs['choices'].insert(0, BLANK_CHOICE_DASH[0])
        return kwargs


class CheckboxesFieldBlock(OptionalFormFieldBlock):
    checkboxes = ListBlock(CharBlock(label=_('Checkbox')))

    field_class = forms.MultipleChoiceField
    widget = forms.CheckboxSelectMultiple

    class Meta:
        label = _('Multiple checkboxes field')
        icon = 'list-ul'

    def get_field_kwargs(self, struct_value):
        kwargs = super(CheckboxesFieldBlock,
                       self).get_field_kwargs(struct_value)
        kwargs['choices'] = [(choice, choice)
                             for choice in struct_value['checkboxes']]
        return kwargs


class DatePickerInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs')
        if attrs is None:
            attrs = {}
        attrs.update({
            'data-provide': 'datepicker',
            'data-date-format': 'yyyy-mm-dd',
        })
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)


class DateFieldBlock(OptionalFormFieldBlock):
    default_value = DateBlock(required=False)

    field_class = forms.DateField
    widget = DatePickerInput

    class Meta:
        label = _('Date field')
        icon = 'date'


class HTML5TimeInput(forms.TimeInput):
    input_type = 'time'


class TimeFieldBlock(OptionalFormFieldBlock):
    default_value = TimeBlock(required=False)

    field_class = forms.TimeField
    widget = HTML5TimeInput

    class Meta:
        label = _('Time field')
        icon = 'time'


class DateTimePickerInput(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        super().__init__(attrs=attrs,
                         date_format=date_format, time_format=time_format)
        self.widgets = (
            DatePickerInput(attrs=attrs, format=date_format),
            HTML5TimeInput(attrs=attrs, format=time_format),
        )

    def decompress(self, value):
        if isinstance(value, str):
            value = parse_datetime(value)
        return super().decompress(value)


class DateTimeFieldBlock(OptionalFormFieldBlock):
    default_value = DateTimeBlock(required=False)

    field_class = forms.SplitDateTimeField
    widget = DateTimePickerInput

    class Meta:
        label = _('Date+time field')
        icon = 'date'


class ImageFieldBlock(OptionalFormFieldBlock):
    field_class = forms.ImageField

    class Meta:
        label = _('Image field')
        icon = 'image'


class FileFieldBlock(OptionalFormFieldBlock):
    field_class = forms.FileField

    class Meta:
        label = _('File field')
        icon = 'download'


class FormFieldsBlock(StreamBlock):
    char = CharFieldBlock(group=_('Fields'))
    text = TextFieldBlock(group=_('Fields'))
    number = NumberFieldBlock(group=_('Fields'))
    checkbox = CheckboxFieldBlock(group=_('Fields'))
    radios = RadioButtonsFieldBlock(group=_('Fields'))
    dropdown = DropdownFieldBlock(group=_('Fields'))
    checkboxes = CheckboxesFieldBlock(group=_('Fields'))
    date = DateFieldBlock(group=_('Fields'))
    time = TimeFieldBlock(group=_('Fields'))
    datetime = DateTimeFieldBlock(group=_('Fields'))
    image = ImageFieldBlock(group=_('Fields'))
    file = FileFieldBlock(group=_('Fields'))
    text_markup = RichTextBlock(group=_('Other'))

    class Meta:
        label = _('Form fields')


class FormStepBlock(StructBlock):
    name = CharBlock(label=_('Name'), required=False)
    form_fields = FormFieldsBlock()

    class Meta:
        label = _('Form step')


class FormStepsBlock(StreamBlock):
    step = FormStepBlock()

    class Meta:
        label = _('Form steps')
