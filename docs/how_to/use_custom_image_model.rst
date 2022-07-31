Using a Custom Image Model in Wagtail CRX
=========================================

.. versionadded:: 0.19

    Added support for custom image models. You must be on Wagtail CRX version
    0.19 or higher in order to follow this guide.

Using a custom image model is a very similar process to using a custom user
model in Django --- it is easy to do when starting a new project but extremely
difficult to do mid-project. This guide will cover starting a **new** project
using a custom image model. To switch to a custom image model mid-project,
see :doc:`convert_image_model`.

Before starting this guide, it is important that you are starting with a fresh
empty database and have **never run wagtailcrx migrations!**


.. include:: _custom_image1.rst

.. include:: _custom_image2.rst

.. include:: _custom_image3.rst


Step 4: Migrate Wagtail CRX
---------------------------

Now you may run **all** migrations which will properly wire everything up to
use your custom image model.

.. code-block:: console

    $ python manage.py migrate
