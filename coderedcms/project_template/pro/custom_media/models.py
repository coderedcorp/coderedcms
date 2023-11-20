"""
Custom overrides of Wagtail Document and Image models. All other
models related to website content should most likely go in
``website.models`` instead.
"""
from django.db import models
from wagtail.documents.models import AbstractDocument
from wagtail.documents.models import Document
from wagtail.images.models import AbstractImage
from wagtail.images.models import AbstractRendition
from wagtail.images.models import Image


class CustomDocument(AbstractDocument):
    """
    A custom Wagtail Document model. Right now it is the same as
    the default, but can be easily extended by adding more fields here.
    """

    admin_form_fields = Document.admin_form_fields


class CustomImage(AbstractImage):
    """
    A custom Wagtail Image model with fields for alt text and
    credit/attribution.
    """

    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt Text",
        help_text=(
            "A description of this image used by search engines and screen readers."
        ),
    )
    credit = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Credit",
        help_text=(
            "Credit or attribute the source of the image. "
            "Properly attributing images taken from online sources can "
            "reduce your risk of copyright infringement."
        ),
    )
    admin_form_fields = Image.admin_form_fields + (
        "alt_text",
        "credit",
    )


class CustomRendition(AbstractRendition):
    """
    Image rendition for our CustomImage model.
    """

    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
