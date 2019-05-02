"""
Blocks module entry point. Used to cleanly organize blocks into
individual files based on purpose, but provide them all as a
single `blocks` module.
"""

from django.utils.translation import ugettext_lazy as _
from wagtail.core.blocks import CharBlock, StreamBlock, StructBlock

from coderedcms.wagtail_flexible_forms.blocks import FormStepBlock, FormStepsBlock

from .advanced_form_blocks import * #noqa
from .base_blocks import * #noqa
from .html_blocks import * #noqa
from .metadata_blocks import * #noqa
from .content_blocks import * #noqa
from .layout_blocks import * #noqa



# Collections of blocks commonly used together.

HTML_STREAMBLOCKS = [
    ('text', RichTextBlock(icon='fa-file-text-o', group=_('HTML'))),
    ('button', ButtonBlock(group=_('HTML'))),
    ('image', ImageBlock(group=_('HTML'))),
    ('image_link', ImageLinkBlock(group=_('HTML'))),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'), group=_('HTML'))),
    ('download', DownloadBlock(group=_('HTML'))),
    ('embed_video', EmbedVideoBlock(group=_('HTML'))),
    ('quote', QuoteBlock(group=_('HTML'))),
    ('table', TableBlock(group=_('HTML'))),
    ('google_map', EmbedGoogleMapBlock(group=_('HTML'))),
    ('page_list', PageListBlock(group=_('HTML'))),
    ('page_preview', PagePreviewBlock(group=_('HTML'))),
]

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + [
    ('card', CardBlock(group=_('Content'))),
    ('carousel', CarouselBlock(group=_('Content'))),
    ('image_gallery', ImageGalleryBlock(group=_('Content'))),
    ('modal', ModalBlock(HTML_STREAMBLOCKS, group=_('Content'))),
    ('pricelist', PriceListBlock(group=_('Content'))),
    ('reusable_content', ReusableContentBlock(group=_('Content'))),
]

NAVIGATION_STREAMBLOCKS = [
    ('page_link', NavPageLinkWithSubLinkBlock(group=_('Navigation'))),
    ('external_link', NavExternalLinkWithSubLinkBlock(group=_('Navigation'))),
    ('document_link', NavDocumentLinkWithSubLinkBlock(group=_('Navigation'))),
]

BASIC_LAYOUT_STREAMBLOCKS = [
    ('row', GridBlock(HTML_STREAMBLOCKS, group=('Layout'))),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'), group=('Layout'))),
]

LAYOUT_STREAMBLOCKS = [
    ('hero', HeroBlock([
        ('row', GridBlock(CONTENT_STREAMBLOCKS)),
        ('cardgrid', CardGridBlock([
            ('card', CardBlock()),])
        ),
        ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),])
    ),
    ('row', GridBlock(CONTENT_STREAMBLOCKS)),
    ('cardgrid', CardGridBlock([
        ('card', CardBlock()),])
    ),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),
]

ADVANCEDFORM_FORMBLOCKS = [
    ('single_line', CoderedAdvancedFormCharFieldBlock(group=_('Fields'))),
    ('multi_line', CoderedAdvancedFormTextFieldBlock(group=_('Fields'))),
    ('number', CoderedAdvancedFormNumberFieldBlock(group=_('Fields'))),
    ('checkbox', CoderedAdvancedFormCheckboxFieldBlock(group=_('Fields'))),
    ('radios', CoderedAdvancedFormRadioButtonsFieldBlock(group=_('Fields'))),
    ('dropdown', CoderedAdvancedFormDropdownFieldBlock(group=_('Fields'))),
    ('checkboxes', CoderedAdvancedFormCheckboxesFieldBlock(group=_('Fields'))),
    ('date', CoderedAdvancedFormDateFieldBlock(group=_('Fields'))),
    ('time', CoderedAdvancedFormTimeFieldBlock(group=_('Fields'))),
    ('datetime', CoderedAdvancedFormDateTimeFieldBlock(group=_('Fields'))),
    ('image', CoderedAdvancedFormImageFieldBlock(group=_('Fields'))),
    ('file', CoderedAdvancedFormFileFieldBlock(group=_('Fields'))),
]


ADVANCEDFORM_STREAMBLOCKS = ADVANCEDFORM_FORMBLOCKS + CONTENT_STREAMBLOCKS

class CoderedAdvancedFormStepBlock(FormStepBlock):
    form_fields = StreamBlock(ADVANCEDFORM_STREAMBLOCKS)


class CoderedAdvancedFormStepsBlock(FormStepsBlock):
    step = CoderedAdvancedFormStepBlock()
