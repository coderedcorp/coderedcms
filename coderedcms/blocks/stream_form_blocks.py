from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks


from coderedcms.wagtail_flexible_forms import blocks as form_blocks
from coderedcms.blocks.base_blocks import BaseBlock, CoderedAdvSettings
from coderedcms.forms import SecureFileField


class CoderedFormAdvSettings(CoderedAdvSettings):

    conditional_name = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Conditional Name'),
        help_text=_('The name used to identify this block for other blocks to target as a condition.')
    )
    conditional_target_name = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Conditional Target Name'),
        help_text=_('The name of the block that will be this block\'s condition.')
    )
    conditional_target_value = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Conditional Target Value'),
        help_text=_('The value of this block\'s condition that is required to show this block on the form.')
    )


class FormBlockMixin(BaseBlock):
    class Meta:
        abstract=True

    advsettings_class = CoderedFormAdvSettings

class CoderedStreamFormFieldBlock(form_blocks.OptionalFormFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormCharFieldBlock(form_blocks.CharFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormTextFieldBlock(form_blocks.TextFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormNumberFieldBlock(form_blocks.NumberFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormCheckboxFieldBlock(form_blocks.CheckboxFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormRadioButtonsFieldBlock(form_blocks.RadioButtonsFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormDropdownFieldBlock(form_blocks.DropdownFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormCheckboxesFieldBlock(form_blocks.CheckboxesFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormDateFieldBlock(form_blocks.DateFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormTimeFieldBlock(form_blocks.TimeFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormDateTimeFieldBlock(form_blocks.DateTimeFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormImageFieldBlock(form_blocks.ImageFieldBlock, FormBlockMixin):
    pass


class CoderedStreamFormFileFieldBlock(form_blocks.FileFieldBlock, FormBlockMixin):
    field_class = SecureFileField

class CoderedStreamFormStepBlock(form_blocks.FormStepBlock):
    form_fields = blocks.StreamBlock()

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(
            local_blocks = [
                ('form_fields', blocks.StreamBlock(local_blocks))
            ]
        )
