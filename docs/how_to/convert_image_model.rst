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


.. include:: _custom_image1.rst

.. include:: _custom_image2.rst

Now, apply the migration:

.. code-block:: console

    $ python manage.py migrate mediamodels

.. include:: _custom_image3.rst


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
