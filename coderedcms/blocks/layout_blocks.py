"""
Layout blocks are essentially a wrapper around content.
e.g. rows, columns, hero units, etc.
"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from coderedcms.settings import crx_settings

from .base_blocks import BaseLayoutBlock
from .base_blocks import CoderedAdvColumnSettings


# Level 1 layout blocks


class ColumnBlock(BaseLayoutBlock):
    """
    Renders content in a column.
    """

    column_size = blocks.ChoiceBlock(
        choices=crx_settings.CRX_FRONTEND_COL_SIZE_CHOICES,
        default=crx_settings.CRX_FRONTEND_COL_SIZE_DEFAULT,
        required=False,
        label=_("Column size"),
    )

    advsettings_class = CoderedAdvColumnSettings

    class Meta:
        template = "coderedcms/blocks/column_block.html"
        icon = "placeholder"
        label = "Column"
        description = "Renders the content in a column."
        preview_value = (
            {
                "settings": {
                    "custom_template": "",
                },
                "content": [("text", "<h1>This is a column!</h1>")],
            },
        )


class GridBlock(BaseLayoutBlock):
    """
    Renders a row of columns.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        label=_("Full width"),
    )

    class Meta:
        template = "coderedcms/blocks/grid_block.html"
        icon = "cr-columns"
        label = _("Responsive Grid Row")
        description = "Renders a row of columns."
        preview_value = {
            "settings": {
                "custom_template": "",
            },
            "content": [
                (
                    "content",
                    {
                        "settings": {
                            "custom_template": "",
                        },
                        "content": [("text", "<h1>This is a row block!</h1>")],
                    },
                ),
                (
                    "content",
                    {
                        "settings": {
                            "custom_template": "",
                        },
                        "content": [("text", "<h1>With Two Columns!</h1>")],
                    },
                ),
            ],
        }

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks=[("content", ColumnBlock(local_blocks))])


class CardGridBlock(BaseLayoutBlock):
    """
    Renders a row of cards.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        label=_("Full width"),
    )

    class Meta:
        template = "coderedcms/blocks/cardgrid_deck.html"
        icon = "cr-th-large"
        label = _("Card Grid")
        description = "Renders a row of cards."
        preview_value = {
            "settings": {"custom_template": ""},
            "content": [
                (
                    "card",
                    {
                        "settings": {"custom_template": ""},
                        "title": "Card 1",
                    },
                ),
                (
                    "card",
                    {
                        "settings": {"custom_template": ""},
                        "title": "Card 2",
                    },
                ),
                (
                    "card",
                    {
                        "settings": {"custom_template": ""},
                        "title": "Card 3",
                    },
                ),
            ],
        }


class HeroBlock(BaseLayoutBlock):
    """
    Wrapper with color and image background options.
    """

    fluid = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Full width"),
    )
    is_parallax = blocks.BooleanBlock(
        required=False,
        label=_("Parallax Effect"),
        help_text=_(
            "Background images scroll slower than foreground images, creating an illusion of depth."
        ),
    )
    background_image = ImageChooserBlock(required=False)
    tile_image = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Tile background image"),
    )
    background_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Background color"),
        help_text=_("Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)"),
    )
    foreground_color = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Text color"),
        help_text=_("Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)"),
    )

    class Meta:
        template = "coderedcms/blocks/hero_block.html"
        icon = "cr-newspaper-o"
        label = "Hero Unit"
        description = "Wrapper with color and image background options."
        preview_value = {
            "settings": {
                "custom_template": "",
            },
            "background_color": "#ff0011",
            "foreground_color": "#ffffff",
            "content": [
                (
                    "row",
                    {
                        "settings": {
                            "custom_template": "",
                        },
                        "content": [
                            (
                                "content",
                                {
                                    "settings": {
                                        "custom_template": "",
                                    },
                                    "content": [
                                        ("text", "<h1>This is a hero block!")
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        }
