Contributing
============


Developing and testing coderedcms
---------------------------------
To create a test project locally before committing your changes:

#. Clone the code from https://github.com/coderedcorp/coderedcms.
#. Run ``pip install -e ./[dev]`` from the root coderedcms directory. The -e flag makes the install editable,
   which is relevant when running makemigrations in test project to actually generate the migration
   files in the coderedcms pip package. The ``[dev]`` installs extras such as sphinx for generating docs.
#. Follow the steps in :doc:`/getting_started/install`. Use "testproject" for
   your project name to ensure it is ignored by git.
#. When making model or block changes within coderedcms, run ``makemigrations coderedcms`` in the
   test project to generate the relevant migration files for the pip package. ALWAYS follow steps
   4 and 5 in :doc:`/getting_started/install` with a fresh database before making migrations.
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
When creating a pull request, please make sure you include the following:

* A description in the pull request of what this change does and how it works.
* Reference to an issue if the change is related to one of the issues on our GitHub page.
* Documentation updates in the ``docs/`` directory describing your change.

Following submission of your pull request, a CodeRed member will review and test your change.
**All changes, even by CodeRed members, must go through a pull request process to ensure quality.**


Versioning
----------

CodeRed CMS follows the ``[major].[minor].[maintenance]`` versioning scheme.

* **Major** version changes mean there is most likely significant changes that may not be backwards
  compatible.
* **Minor** version changes indicate new features, enhancements, and bug fixes that are most likely
  but not guaranteed to be backwards compatible with other releases in the existing major version.
* **Maintenance** version changes are guaranteed to be backwards compatible with other releases with
  the same major and minor version numbers. These changes are reserved for bug, security, or documentation
  fixes only.

.. note::
    CodeRed CMS may have breaking changes between minor version upgrades until reaching a stable
    1.0 status. Releases with a zero major version number are considered "beta" quality.


Building pip packages
---------------------

To build a publicly consumable pip package, run::

    python setup.py sdist bdist_wheel


Building documentation
----------------------

For every code or feature change, be sure to update the docs in the repository. To build and publish
the documentation run::

    cd docs/
    make clean
    make html

Output will be in ``docs/_build/html/`` directory.


Publishing a new release
------------------------

First checkout the code/branch for release.

Next build a pip package::

    python setup.py sdist bdist_wheel

Then upload the pip package to pypi::

    twine upload dist/*

Finally build and update docs::

    cd docs/
    make clean
    make html

If updating docs for an existing minor version release:

#. Copy the contents of ``docs/_build/html/`` to the CodeRed docs server under the existing version directory.

If this is a new major or minor version release:

#. Create a new major.minor directory on the CodeRed docs server.
#. Update the ``stable`` symlink to point to the new version directory.
#. Add the new version to the ``versions.txt`` file on the docs server.
#. Copy the contents of ``docs/_build/html/`` to the CodeRed docs server under the new version directory.

Note that we do not release separate documentation versions for maintenance releases. Update the existing minor
version docs with release notes and other changes.
