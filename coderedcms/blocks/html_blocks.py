"""
HTML blocks are simple blocks used to represent common HTML elements,
with additional styling and attributes.
"""

from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
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
    Emedded media using stock wagtail functionality.
    """
    url = EmbedBlock(
        required=True,
        label=_('URL'),
        help_text=_('Link to a YouTube/Vimeo video, tweet, facebook post, etc.')
    )

    class Meta:
        template = 'coderedcms/blocks/embed_video_block.html'
        icon = 'media'
        label = _('Embed Media')


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
