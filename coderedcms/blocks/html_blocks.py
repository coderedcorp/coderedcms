"""
HTML blocks are simple blocks used to represent common HTML elements,
with additional styling and attributes.

HTML blocks should NOT contain more sub-blocks or sub-streamfields.
They must be safe to nest within more robust "content blocks" without
creating recursion.
"""
import logging
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from .base_blocks import (
    BaseBlock,
    BaseLinkBlock,
    ButtonMixin,
    ClassifierTermChooserBlock,
    CoderedAdvTrackingSettings,
    LinkStructValue,
)


logger = logging.getLogger("coderedcms")


class ButtonBlock(ButtonMixin, BaseLinkBlock):
    """
    A link styled as a button.
    """

    class Meta:
        template = "coderedcms/blocks/button_block.html"
        icon = "cr-hand-pointer-o"
        label = _("Button Link")
        value_class = LinkStructValue


class DownloadBlock(ButtonMixin, BaseBlock):
    """
    Link to a file that can be downloaded.
    """

    downloadable_file = DocumentChooserBlock(
        required=False,
        label=_("Document link"),
    )

    advsettings_class = CoderedAdvTrackingSettings

    class Meta:
        template = "coderedcms/blocks/download_block.html"
        icon = "download"
        label = _("Download")


class EmbedGoogleMapBlock(BaseBlock):
    """
    An embedded Google map in an <iframe>.
    """

    search = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Search query"),
        help_text=_(
            "Address or search term used to find your location on the map."
        ),
    )
    map_title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Map title"),
        help_text=_('Map title for screen readers, ex: "Map to Goodale Park"'),
    )
    place_id = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Google place ID"),
        help_text=_("Requires API key to use place ID."),
    )
    map_zoom_level = blocks.IntegerBlock(
        required=False,
        default=14,
        label=_("Map zoom level"),
        help_text=_(
            "Requires API key to use zoom. "
            "1: World, 5: Landmass/continent, 10: City, 15: Streets, 20: Buildings"
        ),
    )

    class Meta:
        template = "coderedcms/blocks/google_map.html"
        icon = "cr-map"
        label = _("Google Map")


class EmbedVideoBlock(BaseBlock):
    """
    Embedded media using stock wagtail functionality.
    """

    url = EmbedBlock(
        required=True,
        label=_("URL"),
        help_text=_(
            "Link to a YouTube/Vimeo video, tweet, facebook post, etc."
        ),
    )

    class Meta:
        template = "coderedcms/blocks/embed_video_block.html"
        icon = "media"
        label = _("Embed Media")


class H1Block(BaseBlock):
    """
    An <h1> heading.
    """

    text = blocks.CharBlock(
        max_length=255,
        label=_("Text"),
    )

    class Meta:
        template = "coderedcms/blocks/h1_block.html"
        icon = "cr-header"
        label = _("Heading 1")


class H2Block(BaseBlock):
    """
    An <h2> heading.
    """

    text = blocks.CharBlock(
        max_length=255,
        label=_("Text"),
    )

    class Meta:
        template = "coderedcms/blocks/h2_block.html"
        icon = "cr-header"
        label = _("Heading 2")


class H3Block(BaseBlock):
    """
    An <h3> heading.
    """

    text = blocks.CharBlock(
        max_length=255,
        label=_("Text"),
    )

    class Meta:
        template = "coderedcms/blocks/h3_block.html"
        icon = "cr-header"
        label = _("Heading 3")


class TableBlock(BaseBlock):
    table = WagtailTableBlock()

    class Meta:
        template = "coderedcms/blocks/table_block.html"
        icon = "table"
        label = "Table"


class ImageBlock(BaseBlock):
    """
    An <img>, by default styled responsively to fill its container.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )

    class Meta:
        template = "coderedcms/blocks/image_block.html"
        icon = "image"
        label = _("Image")


class ImageLinkBlock(BaseLinkBlock):
    """
    An <a> with an image inside it, instead of text.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )
    alt_text = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=_("Alternate text to show if the image doesn’t load"),
    )

    class Meta:
        template = "coderedcms/blocks/image_link_block.html"
        icon = "image"
        label = _("Image Link")
        value_class = LinkStructValue


class PageListBlock(BaseBlock):
    """
    Renders a preview of selected pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    classified_by = ClassifierTermChooserBlock(
        required=False,
        label=_("Classified as"),
        help_text=_("Only show pages that are classified with this term."),
    )
    # DEPRECATED: Remove in 3.0
    show_preview = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Show body preview"),
    )
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "coderedcms/blocks/pagelist_block.html"
        icon = "list-ul"
        label = _("Latest Pages")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        # try to use the CoderedPage `get_index_children()`,
        # but fall back to get_children if this is a non-CoderedPage
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
            if value["classified_by"]:
                try:
                    pages = pages.filter(
                        classifier_terms=value["classified_by"]
                    )
                except AttributeError:
                    # `pages` is not a queryset, or is not a queryset of CoderedPage.
                    logger.warning(
                        (
                            "Tried to filter by ClassifierTerm in PageListBlock, "
                            "but <%s.%s ('%s')>.get_index_children() "
                            "did not return a queryset or is not a queryset of "
                            "CoderedPage models."
                        ),
                        indexer._meta.app_label,
                        indexer.__class__.__name__,
                        indexer.title,
                    )
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context


class PagePreviewBlock(BaseBlock):
    """
    Renders a preview of a specific page.
    """

    page = blocks.PageChooserBlock(
        required=True,
        label=_("Page to preview"),
        help_text=_("Show a mini preview of the selected page."),
    )

    class Meta:
        template = "coderedcms/blocks/pagepreview_block.html"
        icon = "doc-empty-inverse"
        label = _("Page Preview")


class QuoteBlock(BaseBlock):
    """
    A <blockquote>.
    """

    text = blocks.TextBlock(
        required=True,
        rows=4,
        label=_("Quote Text"),
    )
    author = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Author"),
    )

    class Meta:
        template = "coderedcms/blocks/quote_block.html"
        icon = "openquote"
        label = _("Quote")


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = "coderedcms/blocks/rich_text_block.html"
