"""
HTML blocks are simple blocks used to represent common HTML elements,
with additional styling and attributes.
"""

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from pygments import highlight
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from .base_blocks import BaseBlock, BaseLinkBlock, ButtonMixin, CoderedAdvTrackingSettings, LinkStructValue


class ButtonBlock(ButtonMixin, BaseLinkBlock):
    """
    A link styled as a button.
    """
    class Meta:
        template = 'coderedcms/blocks/button_block.html'
        icon = 'fa-hand-pointer-o'
        label = _('Button Link')
        value_class = LinkStructValue


class CodeBlock(BaseBlock):
    """
    Source code with syntax highlighting in a <pre> tag.
    """
    LANGUAGE_CHOICES = []

    for lex in get_all_lexers():
        LANGUAGE_CHOICES.append((lex[1][0], lex[0]))

    language = blocks.ChoiceBlock(
        required=False,
        choices=LANGUAGE_CHOICES,
        label=_('Syntax highlighting'),
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Title'),
    )
    code = blocks.TextBlock(
        classname='monospace',
        rows=8,
        label=('Code'),
        help_text=_('Code is rendered in a <pre> tag.'),
    )

    def get_context(self, value, parent_context=None):
        ctx = super(CodeBlock, self).get_context(value, parent_context)

        if value['language']:
            src = value['code'].strip('\n')
            lexer = get_lexer_by_name(value['language'])
            code_html = mark_safe(highlight(src, lexer, HtmlFormatter()))
        else:
            code_html = format_html('<pre>{}</pre>', value['code'])

        ctx.update({
            'code_html': code_html,
        })

        return ctx

    class Meta:
        template = 'coderedcms/blocks/code_block.html'
        icon = 'fa-file-code-o'
        label = _('Formatted Code')


class DownloadBlock(ButtonMixin, BaseBlock):
    """
    Link to a file that can be downloaded.
    """
    automatic_download = blocks.BooleanBlock(
        required=False,
        label=_('Auto download'),
    )
    downloadable_file = DocumentChooserBlock(
        required=False,
        label=_('Document link'),
    )

    advsettings_class = CoderedAdvTrackingSettings

    class Meta:
        template = 'coderedcms/blocks/download_block.html'
        icon = 'download'
        label = _('Download')


class EmbedGoogleMapBlock(BaseBlock):
    """
    An embedded Google map in an <iframe>.
    """
    search = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Search query'),
        help_text=_('Address or search term used to find your location on the map.'),
    )
    api_key = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('API key'),
        help_text=_('Optional. Only required to use place ID and zoom features.')
    )
    place_id = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Google place ID'),
        help_text=_('Requires API key to use place ID.')
    )
    map_zoom_level = blocks.IntegerBlock(
        required=False,
        default=14,
        label=_('Map zoom level'),
        help_text=_('Requires API key to use zoom. 1: World, 5: Landmass/continent, 10: City, 15: Streets, 20: Buildings')
    )

    class Meta:
        template = 'coderedcms/blocks/google_map.html'
        icon = 'fa-map'
        label = _('Google Map')


class EmbedVideoBlock(BaseBlock):
    """
    An embedded video on the page in an <iframe>. Currently supports youtube and vimeo.
    """
    url = blocks.URLBlock(
        required=True,
        label=_('URL'),
        help_text=_('Link to a YouTube or Vimeo video.'),
    )

    class Meta:
        template = 'coderedcms/blocks/embed_video_block.html'
        icon = 'media'
        label = _('Embed Video')


class H1Block(BaseBlock):
    """
    An <h1> heading.
    """
    text = blocks.CharBlock(
        max_length=255,
        label=_('Text'),
    )

    class Meta:
        template = 'coderedcms/blocks/h1_block.html'
        icon = 'fa-header'
        label = _('Heading 1')


class H2Block(BaseBlock):
    """
    An <h2> heading.
    """
    text = blocks.CharBlock(
        max_length=255,
        label=_('Text'),
    )

    class Meta:
        template = 'coderedcms/blocks/h2_block.html'
        icon = 'fa-header'
        label = _('Heading 2')


class H3Block(BaseBlock):
    """
    An <h3> heading.
    """
    text = blocks.CharBlock(
        max_length=255,
        label=_('Text'),
    )

    class Meta:
        template = 'coderedcms/blocks/h3_block.html'
        icon = 'fa-header'
        label = _('Heading 3')


class TableBlock(BaseBlock):
    table = WagtailTableBlock()

    class Meta:
        template = 'coderedcms/blocks/table_block.html'
        icon = 'fa-table'
        label = 'Table'


class ImageBlock(BaseBlock):
    """
    An <img>, by default styled responsively to fill its container.
    """
    image = ImageChooserBlock(
        label=_('Image'),
    )

    class Meta:
        template = 'coderedcms/blocks/image_block.html'
        icon = 'image'
        label = _('Image')


class ImageLinkBlock(BaseLinkBlock):
    """
    An <a> with an image inside it, instead of text.
    """
    image = ImageChooserBlock(
        label=_('Image'),
    )
    alt_text = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=_('Alternate text to show if the image doesn’t load'),
    )

    class Meta:
        template = 'coderedcms/blocks/image_link_block.html'
        icon = 'image'
        label = _('Image Link')
        value_class = LinkStructValue


class QuoteBlock(BaseBlock):
    """
    A <blockquote>.
    """
    text = blocks.TextBlock(
        required=True,
        rows=4,
        label=_('Quote Text'),
    )
    author = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Author'),
    )

    class Meta:
        template = 'coderedcms/blocks/quote_block.html'
        icon = 'openquote'
        label = _('Quote')
