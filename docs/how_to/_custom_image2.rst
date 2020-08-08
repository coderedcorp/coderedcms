Step 2: Make migrations
-----------------------

**Before** switching your project to the new custom model, first make a
migration for this model. If your custom image model already exists and has
already been migrated, you can skip this step.

.. code-block:: console

    $ python manage.py makemigrations mediamodels
