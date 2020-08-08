Step 1: Create a custom image model in a new app
------------------------------------------------

It is imperative that the custom image model lives in a Django app which does
not rely on or import ``coderedcms``. It is recommended to create a separate
"pure" app to contain custom image and document models for your site. Failure
to separate the custom image model will create a circular dependency issue in
migrations.

Create an empty Django app, ours will be named ``mediamodels``:

.. code-block:: console

    $ django-admin startapp mediamodels

In ``mediamodels/models.py``, add your custom image model code, following the
`Wagtail custom image sample code <https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html>`_:

.. code-block:: python

    # models.py

    from django.db import models
    from wagtail.images.models import Image, AbstractImage, AbstractRendition


    class CustomImage(AbstractImage):
        # Add any extra fields to image here

        # eg. To add a caption field:
        # caption = models.CharField(max_length=255, blank=True)

        admin_form_fields = Image.admin_form_fields + (
            # Then add the field names here to make them appear in the form:
            # 'caption',
        )


    class CustomRendition(AbstractRendition):
        image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

        class Meta:
            unique_together = (
                ('image', 'filter_spec', 'focal_point_key'),
            )
