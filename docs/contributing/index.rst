Contributing
============

Developing and testing coderedcms
---------------------------------
To create a test project locally before committing your changes:

#. Run ``pip install -e ./[dev]`` from the coderedcms directory. The -e flag makes the install editable,
   which is relevant when running makemigrations in test project to actually generate the migration
   files in the coderedcms pip package. The ``[dev]`` installs extras such as sphinx for generating docs.
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

Contributor guidelines
----------------------

We are happy to accept pull requests from the community if it aligns with our vision for coderedcms.
When created a pull request, please make sure you include the following:

* A description in the pull request of what this change does and how it works.
* Reference to an issue if the change is related to one of the issues on our github page.
* Documentation updates describing your change.

Following submission of your pull request, a CodeRed member will review and test your change.

**All changes, even by CodeRed members, must go through a pull request process to ensure quality.**

Building pip packages
---------------------

To build a publicly consumable pip package and upload to pypi, run::

    python setup.py sdist bdist_wheel
    twine upload dist/*

Building & publishing documentation
-----------------------------------

For every code or feature change, be sure to update the docs in the repository. To build and publish
the documentation run::

    cd docs/
    make clean
    make html

Output will be in ``docs/_build/html/`` directory. To publish:

* If updating docs for an existing minor version release:
    #. Copy the contents of ``docs/_build/html/`` to the CodeRed docs server under the existing version directory.

* If this is a new major or minor version release:
    #. Create a new major.minor directory on the CodeRed docs server.
    #. Update the ``.htaccess`` file to point to the new version directory.
    #. Add the new version to the ``versions.txt`` file on the docs server.
    #. Copy the contents of ``docs/_build/html`` to the CodeRed docs server under the new version directory.

Note that we do not release separate documentation for maintenance releases. Just update the existing minor
version docs if there are any maintenance release doc changes.
