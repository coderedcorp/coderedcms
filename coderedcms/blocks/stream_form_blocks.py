from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks

from coderedcms.wagtail_flexible_forms import blocks as form_blocks
from coderedcms.blocks.base_blocks import BaseBlock, CoderedAdvSettings
from coderedcms.forms import (
    CoderedDateField, CoderedDateInput,
    CoderedDateTimeField, CoderedDateTimeInput,
    CoderedTimeField, CoderedTimeInput,
    SecureFileField
)


class CoderedFormAdvSettings(CoderedAdvSettings):

    condition_trigger_id = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Condition Trigger ID'),
        help_text=_(
            'The "Custom ID" of another field that that will trigger this field to be shown/hidden.')  # noqa
    )
    condition_trigger_value = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Condition Trigger Value'),
        help_text=_(
            'The value of the field in "Condition Trigger ID" that will trigger this field to be shown.')  # noqa
    )


class FormBlockMixin(BaseBlock):
    class Meta:
        abstract = True

    advsettings_class = CoderedFormAdvSettings


class CoderedStreamFormFieldBlock(form_blocks.OptionalFormFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormCharFieldBlock(form_blocks.CharFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Text or Email input")
        icon = "fa-window-minimize"


class CoderedStreamFormTextFieldBlock(form_blocks.TextFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Multi-line text")
        icon = "fa-align-left"


class CoderedStreamFormNumberFieldBlock(form_blocks.NumberFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Numbers only")
        icon = "fa-hashtag"


class CoderedStreamFormCheckboxFieldBlock(form_blocks.CheckboxFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Single Checkbox")
        icon = "fa-check-square-o"


class CoderedStreamFormRadioButtonsFieldBlock(form_blocks.RadioButtonsFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Radios")
        icon = "fa-list-ul"


class CoderedStreamFormDropdownFieldBlock(form_blocks.DropdownFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Dropdown")
        icon = "fa-list-alt"


class CoderedStreamFormCheckboxesFieldBlock(form_blocks.CheckboxesFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Checkboxes")
        icon = "fa-list-ul"


class CoderedStreamFormDateFieldBlock(form_blocks.DateFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Date")
        icon = "fa-calendar"

    field_class = CoderedDateField
    widget = CoderedDateInput


class CoderedStreamFormTimeFieldBlock(form_blocks.TimeFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Time")
        icon = "fa-clock-o"

    field_class = CoderedTimeField
    widget = CoderedTimeInput


class CoderedStreamFormDateTimeFieldBlock(form_blocks.DateTimeFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Date and Time")
        icon = "fa-calendar"

    field_class = CoderedDateTimeField
    widget = CoderedDateTimeInput


class CoderedStreamFormImageFieldBlock(form_blocks.ImageFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Image Upload")
        icon = "fa-picture-o"


class CoderedStreamFormFileFieldBlock(form_blocks.FileFieldBlock, FormBlockMixin):
    class Meta:
        label = _("Secure File Upload")
        icon = "fa-upload"

    field_class = SecureFileField


class CoderedStreamFormStepBlock(form_blocks.FormStepBlock):
    form_fields = blocks.StreamBlock()

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(
            local_blocks=[
                ('form_fields', blocks.StreamBlock(local_blocks))
            ]
        )
