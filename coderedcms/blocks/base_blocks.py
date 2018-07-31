"""
Bases, mixins, and utilites for blocks.
"""

from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks
from wagtail.core.models import Collection
from wagtail.documents.blocks import DocumentChooserBlock

from coderedcms.settings import cr_settings


class MultiSelectBlock(blocks.FieldBlock):
    """
    Renders as MultipleChoiceField, used for adding checkboxes,
    radios, or multiselect inputs in the streamfield.
    """
    def __init__(self, required=True, help_text=None, choices=None, widget=None, **kwargs):
        self.field = forms.MultipleChoiceField(
            required=required,
            help_text=help_text,
            choices=choices,
            widget=widget,
        )
        super().__init__(**kwargs)

    def get_searchable_content(self, value):
        return [force_text(value)]


class CollectionChooserBlock(blocks.ChooserBlock):
    """
    Enables choosing a wagtail Collection in the streamfield.
    """
    target_model = Collection
    widget = forms.Select

    def value_for_form(self, value):
        if isinstance(value, self.target_model):
            return value.pk
        return value


class ButtonMixin(blocks.StructBlock):
    """
    Standard style and size options for buttons.
    """
    button_title = blocks.CharBlock(
        max_length=255,
        required=True,
        label=_('Button Title'),
    )
    button_style = blocks.ChoiceBlock(
        choices=cr_settings['FRONTEND_BTN_STYLE_CHOICES'],
        default=cr_settings['FRONTEND_BTN_STYLE_DEFAULT'],
        required=False,
        label=_('Button Style'),
    )
    button_size = blocks.ChoiceBlock(
        choices=cr_settings['FRONTEND_BTN_SIZE_CHOICES'],
        default=cr_settings['FRONTEND_BTN_SIZE_DEFAULT'],
        required=False,
        label=_('Button Size'),
    )


class CoderedAdvSettings(blocks.StructBlock):
    """
    Common fields each block should have,
    which are hidden under the block's "Advanced Settings" dropdown.
    """
    # placeholder, real value get set in __init__()
    custom_template = blocks.Block()

    custom_css_class = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Custom CSS Class'),
    )
    custom_id = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Custom ID'),
    )

    class Meta:
        form_template = 'wagtailadmin/block_forms/base_block_settings_struct.html'
        label = _('Advanced Settings')

    def __init__(self, local_blocks=None, template_choices=None, **kwargs):
        if not local_blocks:
            local_blocks = ()

        local_blocks += (
            (
                'custom_template',
                blocks.ChoiceBlock(
                    choices=template_choices,
                    default=None,
                    required=False,
                    label=_('Template'))
            ),
        )

        super().__init__(local_blocks, **kwargs)


class CoderedAdvTrackingSettings(CoderedAdvSettings):
    """
    CoderedAdvSettings plus additional tracking fields.
    """
    ga_tracking_event_category = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Tracking Event Category'),
    )
    ga_tracking_event_label = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Tracking Event Label'),
    )


class CoderedAdvColumnSettings(CoderedAdvSettings):
    """
    BaseBlockSettings plus additional column fields.
    """
    column_breakpoint = blocks.ChoiceBlock(
        choices=cr_settings['FRONTEND_COL_BREAK_CHOICES'],
        default=cr_settings['FRONTEND_COL_BREAK_DEFAULT'],
        required=False,
        verbose_name=_('Column Breakpoint'),
        help_text=_('Screen size at which the column will expand horizontally or stack vertically.'),
    )


class BaseBlock(blocks.StructBlock):
    """
    Common attributes for all blocks used in CodeRed CMS.
    """
    # subclasses can override this to determine the advanced settings class
    advsettings_class = CoderedAdvSettings

    # placeholder, real value get set in __init__() from advsettings_class
    settings = blocks.Block()

    def __init__(self, local_blocks=None, **kwargs):
        """
        Construct and inject settings block, then initialize normally.
        """
        klassname = self.__class__.__name__.lower()
        choices = cr_settings['FRONTEND_TEMPLATES_BLOCKS'].get('*', ()) + \
                  cr_settings['FRONTEND_TEMPLATES_BLOCKS'].get(klassname, ())

        if not local_blocks:
            local_blocks = ()

        local_blocks += (('settings', self.advsettings_class(template_choices=choices)),)

        super().__init__(local_blocks, **kwargs)

    def render(self, value, context=None):
        template = value['settings']['custom_template']

        if not template:
            template = self.get_template(context=context)
            if not template:
                return self.render_basic(value, context=context)

        if context is None:
            new_context = self.get_context(value)
        else:
            new_context = self.get_context(value, parent_context=dict(context))

        return mark_safe(render_to_string(template, new_context))


class BaseLayoutBlock(BaseBlock):
    """
    Common attributes for all blocks used in CodeRed CMS.
    """
    # Subclasses can override this to provide a default list of blocks for the content.
    content_streamblocks = []

    def __init__(self, local_blocks=None, **kwargs):
        if not local_blocks and self.content_streamblocks:
            local_blocks = self.content_streamblocks

        if local_blocks:
            local_blocks = (('content', blocks.StreamBlock(local_blocks, label=_('Content'))),)

        super().__init__(local_blocks, **kwargs)


class LinkStructValue(blocks.StructValue):
    """
    Generates a URL for blocks with multiple link choices.
    """
    @property
    def url(self):
        page = self.get('page_link')
        doc = self.get('doc_link')
        ext = self.get('other_link')
        if page:
            return page.url
        elif doc:
            return doc.url
        else:
            return ext

class BaseLinkBlock(BaseBlock):
    """
    Common attributes for creating a link within the CMS.
    """
    page_link = blocks.PageChooserBlock(
        required=False,
        label=_('Page link'),
    )
    doc_link = DocumentChooserBlock(
        required=False,
        label=_('Document link'),
    )
    other_link = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Other link'),
    )

    advsettings_class = CoderedAdvTrackingSettings

    class Meta:
        value_class = LinkStructValue

