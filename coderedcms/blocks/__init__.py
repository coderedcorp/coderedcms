"""
Blocks module entry point. Used to cleanly organize blocks into
individual files based on purpose, but provide them all as a
single `blocks` module.
"""

from django.utils.translation import ugettext_lazy as _

from .base_blocks import * #noqa
from .html_blocks import * #noqa
from .metadata_blocks import * #noqa
from .content_blocks import * #noqa
from .layout_blocks import * #noqa


# Collections of blocks commonly used together.

HTML_STREAMBLOCKS = [
    ('text', blocks.RichTextBlock(icon='fa-file-text-o')),
    ('button', ButtonBlock()),
    ('image', ImageBlock()),
    ('image_link', ImageLinkBlock()),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),
    ('download', DownloadBlock()),
    ('embed_video', EmbedVideoBlock()),
    ('quote', QuoteBlock()),
    ('table', TableBlock()),
    ('google_map', EmbedGoogleMapBlock()),
]

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + [
    ('card', CardBlock()),
    ('carousel', CarouselBlock()),
    ('image_gallery', ImageGalleryBlock()),
    ('page_list', PageListBlock()),
    ('modal', ModalBlock(HTML_STREAMBLOCKS)),
    ('pricelist', PriceListBlock()),
    ('reusable_content', ReusableContentBlock()),
]

NAVIGATION_STREAMBLOCKS = [
    ('page_link', NavPageLinkWithSubLinkBlock()),
    ('external_link', NavExternalLinkWithSubLinkBlock()),
    ('document_link', NavDocumentLinkWithSubLinkBlock()),
]

BASIC_LAYOUT_STREAMBLOCKS = [
    ('row', GridBlock(HTML_STREAMBLOCKS)),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),
]

LAYOUT_STREAMBLOCKS = [
    ('row', GridBlock(CONTENT_STREAMBLOCKS)),
    ('cardgrid', CardGridBlock([
        ('card', CardBlock()),])
    ),
    ('hero', HeroBlock([
        ('row', GridBlock(CONTENT_STREAMBLOCKS)),
        ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),])
    ),
    ('html', blocks.RawHTMLBlock(icon='code', classname='monospace', label=_('HTML'))),
]
