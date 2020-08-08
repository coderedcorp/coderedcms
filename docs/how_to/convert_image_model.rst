Convert Existing Site to Use a Custom Image Model
=================================================

.. versionadded:: 0.19

    Added support for custom image models. You must be on CodeRed CMS version
    0.19 or higher in order to follow this guide.

Using a custom image model is a very similar process to using a custom user
model in Django --- it is easy to do when starting a new project but extremely
difficult to do mid-project. This process requires deep understanding of the
Django ORM, SQL, and relational database design. It is therefore recommended to
truly evaluate if and why you really need to switch to a custom image model. If
you're simply looking to store metadata about an image, the same effect could be
much more easily achieved with a separate "metadata" model with a `OneToOne
<https://docs.djangoproject.com/en/stable/topics/db/examples/one_to_one/>`_
relationship to the Image model, and do a reverse lookup (e.g.
``image.metadata``).

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


Step 4: Migrate your models and database schema by hand
-------------------------------------------------------

At this point the database tables of existing coderedcms models have FK pointing
to ``wagtailimages.Image``, however Django thinks they are pointing to the new
custom image table, hence creating FOREIGN KEY constraint problems.

For this same reason, running ``makemigrations`` will yield "No changes
detected" as the Django ORM has no knowledge that the foreign keys are pointing
to the wrong tables. Hence the database schema must be changed by hand.

The end result is your existing image database tables should be moved to the new
custom image table, and every current table with a foreign key to the old image
table needs to be updated as a foreign key to the new image table.

This process will differ from project to project, so you will need to find your
own way to update the database schema that fits your project. Many related
discussions about switching the Django User model (replace "user" with "image"
in this context) can be found online and are highly relevant and helpful. Start
by reading `Django ticket #25313 <https://code.djangoproject.com/ticket/25313>`_
on the subject.

To help with your database update, below is a list of each concrete CodeRed
model which references the Image. A `search query of the source code
<https://github.com/coderedcorp/coderedcms/search?l=Python&q=get_image_model_string>`_
can also yield specific results.

* ``coderedcms.models.CoderedPage.cover_image``

* ``coderedcms.models.CoderedPage.og_image``

* ``coderedcms.models.CoderedPage.struct_org_logo``

* ``coderedcms.models.CoderedPage.struct_org_image``

* ``coderedcms.models.CarouselSlide.image``

* ``coderedcms.models.LayoutSettings.logo``

* ``coderedcms.models.LayoutSettings.favicon``
