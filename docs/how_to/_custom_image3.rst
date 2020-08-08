Step 3: Switch to the new image model
-------------------------------------

In your Django settings file, (probably under ``settings/base.py``) set the
``WAGTAILIMAGES_IMAGE_MODEL`` setting to point to it:

.. code-block:: python

    WAGTAILIMAGES_IMAGE_MODEL = "mediamodels.CustomImage"
