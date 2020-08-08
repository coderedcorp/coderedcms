Convert Existing Site to Use a Custom Image Model
=================================================

.. versionadded:: 0.19

    Added support for custom image models. You must be on CodeRed CMS version
    0.19 or higher in order to follow this guide.

Before starting this guide, ensure you have updated to the latest CodeRed CMS,
have run all migrations, and do not have any pending migrations.

.. code-block:: console

    $ python manage.py migrate
    $ python manage.py makemigrations
    No changes detected


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


Step 2: Make migrations
-----------------------

**Before** switching your project to the new custom model, first make a
migration for this model. If your custom image model already exists and has
already been migrated, you can skip this step.

.. code-block:: console

    $ python manage.py makemigrations mediamodels
    $ python manage.py migrate mediamodels


Step 3: Switch to the new image model
-------------------------------------

In your Django settings file, (probably under ``settings/base.py``) set the
``WAGTAILIMAGES_IMAGE_MODEL`` setting to point to it:

.. code-block:: python

    WAGTAILIMAGES_IMAGE_MODEL = "mediamodels.CustomImage"


Step 4: Encounter Database Errors [TODO]
----------------------------------------

At this point the database tables of existing coderedcms models have FK pointing
to ``wagtailimages.Image``, however Django thinks they are pointing to the new
custom image table, hence creating FOREIGN KEY constraint problems.

Some ideas for next steps:

* Create a hand-made migrations to manually convert all coderedcms models to use
  the new image, since Django does not seem to be able to figure this out.

* User will also inevitably have to create a custom migration in their own app
  to convert their existing models to use the new image. This will probably be
  more straightforward though since they would not be using swappable dependency
  in their migrations.
