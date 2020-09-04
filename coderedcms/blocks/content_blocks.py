"""
Content blocks are for building complex, nested HTML structures that usually
contain sub-blocks, and may require javascript to function properly.
"""
from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from .base_blocks import BaseBlock, BaseLayoutBlock, ButtonMixin, CollectionChooserBlock
from .html_blocks import ButtonBlock


class CardBlock(BaseBlock):
    """
    A component of information with image, text, and buttons.
    """
    image = ImageChooserBlock(
        required=False,
        max_length=255,
        label=_('Image'),
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Title'),
    )
    subtitle = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Subtitle'),
    )
    description = blocks.RichTextBlock(
        features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link'],
        label=_('Body'),
    )
    links = blocks.StreamBlock(
        [('Links', ButtonBlock())],
        blank=True,
        required=False,
        label=_('Links'),
    )

    class Meta:
        template = 'coderedcms/blocks/card_foot.html'
        icon = 'fa-list-alt'
        label = _('Card')


class CarouselBlock(BaseBlock):
    """
    Enables choosing a Carousel snippet.
    """
    carousel = SnippetChooserBlock('coderedcms.Carousel')

    class Meta:
        icon = 'image'
        label = _('Carousel')
        template = 'coderedcms/blocks/carousel_block.html'


class ImageGalleryBlock(BaseBlock):
    """
    Show a collection of images with interactive previews that expand to
    full size images in a modal.
    """
    collection = CollectionChooserBlock(
        required=True,
        label=_('Image Collection'),
    )

    class Meta:
        template = 'coderedcms/blocks/image_gallery_block.html'
        icon = 'image'
        label = _('Image Gallery')


class ModalBlock(ButtonMixin, BaseLayoutBlock):
    """
    Renders a button that then opens a popup/modal with content.
    """
    header = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Modal heading'),
    )
    content = blocks.StreamBlock(
        [],
        label=_('Modal content'),
    )
    footer = blocks.StreamBlock(
        [
            ('text', blocks.CharBlock(icon='fa-file-text-o', max_length=255, label=_('Simple Text'))),  # noqa
            ('button', ButtonBlock()),
        ],
        required=False,
        label=_('Modal footer'),
    )

    class Meta:
        template = 'coderedcms/blocks/modal_block.html'
        icon = 'fa-window-maximize'
        label = _('Modal')


class NavBaseLinkBlock(BaseBlock):
    display_text = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Display text'),
    )
    image = ImageChooserBlock(
        required=False,
        label=_('Image'),
    )


class NavExternalLinkBlock(NavBaseLinkBlock):
    """
    External link.
    """
    link = blocks.CharBlock(
        required=False,
        label=_('URL'),
    )

    class Meta:
        template = 'coderedcms/blocks/external_link_block.html'
        label = _('External Link')


class NavPageLinkBlock(NavBaseLinkBlock):
    """
    Page link.
    """
    page = blocks.PageChooserBlock(
        label=_('Page'),
    )

    class Meta:
        template = 'coderedcms/blocks/page_link_block.html'
        label = _('Page Link')


class NavDocumentLinkBlock(NavBaseLinkBlock):
    """
    Document link.
    """
    document = DocumentChooserBlock(
        label=_('Document'),
    )

    class Meta:
        template = 'coderedcms/blocks/document_link_block.html'
        label = _('Document Link')


class NavSubLinkBlock(BaseBlock):
    """
    Streamblock for rendering nested sub-links.
    """
    sub_links = blocks.StreamBlock(
        [
            ('page_link', NavPageLinkBlock()),
            ('external_link', NavExternalLinkBlock()),
            ('document_link', NavDocumentLinkBlock()),
        ],
        required=False,
        label=_('Sub-links'),
    )


class NavExternalLinkWithSubLinkBlock(NavSubLinkBlock, NavExternalLinkBlock):
    """
    Extermal link with option for sub-links.
    """
    class Meta:
        label = _('External link with sub-links')


class NavPageLinkWithSubLinkBlock(NavSubLinkBlock, NavPageLinkBlock):
    """
    Page link with option for sub-links or showing child pages.
    """
    show_child_links = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_('Show child pages'),
        help_text=_('Automatically show a link to the Page’s child pages as a dropdown menu.'),
    )

    class Meta:
        label = _('Page link with sub-links')


class NavDocumentLinkWithSubLinkBlock(NavSubLinkBlock, NavDocumentLinkBlock):
    """
    Document link with option for sub-links.
    """
    class Meta:
        label = _('Document link with sub-links')


class PriceListItemBlock(BaseBlock):
    """
    Represents one item in a PriceListBlock, such as an entree in a restaurant menu.
    """
    image = ImageChooserBlock(
        required=False,
        label=_('Image'),
    )
    name = blocks.CharBlock(
        required=True,
        max_length=255,
        label=_('Name'),
    )
    description = blocks.TextBlock(
        required=False,
        rows=4,
        label=_('Description'),
    )
    price = blocks.CharBlock(
        required=True,
        label=_('Price'),
        help_text=_('Any text here. Include currency sign if desired.'),
    )

    class Meta:
        template = 'coderedcms/blocks/pricelistitem_block.html'
        icon = 'fa-usd'
        label = _('Price List Item')


class PriceListBlock(BaseBlock):
    """
    A price list, such as a menu for a restaurant.
    """
    heading = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Heading'),
    )
    items = blocks.StreamBlock(
        [
            ('item', PriceListItemBlock()),
        ],
        label=_('Items'),
    )

    class Meta:
        template = 'coderedcms/blocks/pricelist_block.html'
        icon = 'fa-usd'
        label = _('Price List')


class ContentWallBlock(BaseBlock):
    """
    Enables choosing a ContentWall snippet.
    """
    content_wall = SnippetChooserBlock('coderedcms.ContentWall')
    show_content_wall_on_children = blocks.BooleanBlock(
        required=False,
        default=False,
        verbose_name=_('Show content walls on children pages?'),
        help_text=_(
            'If this is checked, the content walls will be displayed on all children pages of this page.')  # noqa
    )

    class Meta:
        icon = 'fa-stop'
        label = _('Content Wall')
        template = 'coderedcms/blocks/content_wall_block.html'


class ReusableContentBlock(BaseBlock):
    """
    Enables choosing a ResusableContent snippet.
    """
    content = SnippetChooserBlock('coderedcms.ReusableContent')

    class Meta:
        icon = 'fa-recycle'
        label = _('Reusable Content')
        template = 'coderedcms/blocks/reusable_content_block.html'
