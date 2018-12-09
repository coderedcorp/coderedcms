Contributing
============

Developing and testing coderedcms
---------------------------------
To create a test project locally before committing your changes:

#. Run ``pip install -e ./`` from the coderedcms directory. The -e flag makes the install editable,
   which is relevant when running makemigrations in test project to actually generate the migration
   files in the coderedcms pip package.
#. Follow steps 4 through 6 in :doc:`/getting_started/index`. Use "testproject" or "testapp" for
   your project name to ensure it is ignored by git.
#. When making model or block changes within coderedcms, run ``makemigrations coderedcms`` in the
   test project to generate the relevant migration files for the pip package. ALWAYS follow steps
   4 and 5 in :doc:`/getting_started/index` with a fresh database before making migrations.
#. When model or block changes affect the local test project (i.e. the "website" app), run
   ``makemigrations website`` in the test project to generate the relevant migration files locally.
   Apply and test the migrations. When satisfied, copy the new migration files to the
   ``project_template/website/migrations/`` directory.

When making changes that are potentially destructive or backwards incompatible, increment the minor
version number until coderedcms reaches a stable 1.0 release. Each production project that uses
coderedcms should specify the appropriate version in its requirements.txt to prevent breakage.

Building pip packages
---------------------

To build a publicly consumable pip package, run::

    python setup.py sdist bdist_wheel

which will build a source distribution and a wheel in the ``dist/`` directory.
