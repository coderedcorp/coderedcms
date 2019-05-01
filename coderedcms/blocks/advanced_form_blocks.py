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


class CoderedAdvancedFormFieldBlock(form_blocks.OptionalFormFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormCharFieldBlock(form_blocks.CharFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormTextFieldBlock(form_blocks.TextFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormNumberFieldBlock(form_blocks.NumberFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormCheckboxFieldBlock(form_blocks.CheckboxFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormRadioButtonsFieldBlock(form_blocks.RadioButtonsFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormDropdownFieldBlock(form_blocks.DropdownFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormCheckboxesFieldBlock(form_blocks.CheckboxesFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormDateFieldBlock(form_blocks.DateFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormTimeFieldBlock(form_blocks.TimeFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormDateTimeFieldBlock(form_blocks.DateTimeFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormImageFieldBlock(form_blocks.ImageFieldBlock, FormBlockMixin):
    pass


class CoderedAdvancedFormFileFieldBlock(form_blocks.FileFieldBlock, FormBlockMixin):
    field_class = SecureFileField
