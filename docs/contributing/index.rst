Contributing
============


Developing Wagtail CRX
----------------------

To create a test project locally:

#. Clone the code from https://github.com/coderedcorp/coderedcms (main branch).
#. Run ``pip install -r requirements-dev.txt`` from the root coderedcms
   directory. This will install development tools, and also make the install
   editable, which is relevant when running ``makemigrations`` in test project
   to actually generate the migration files in the coderedcms pip package.
#. Follow the steps in :doc:`/getting_started/install`. Use ``testproject`` for
   your project name to ensure it is ignored by git.
#. When making model or block changes within coderedcms, run
   ``makemigrations coderedcms`` in the test project to generate the relevant
   migration files for the pip package. ALWAYS follow steps 4 and 5 in
   :doc:`/getting_started/install` with a fresh database before making migrations.
#. When model or block changes affect the local test project (i.e. the "website"
   app), run ``makemigrations website`` in the test project to generate the
   relevant migration files locally. Apply and test the migrations. When
   satisfied, re-generate the ``0001_initial.py`` migration in
   ``project_template/website/migrations/`` as so:

       #. Create a new test project using ``coderedcms start testproject``.
       #. Before running migrations, DELETE all migrations in
          ``testproject/website/migrations/``.
       #. Run ``python manage.py makemigrations website``. This should generate
          an ``0001_initial.py`` migration.
       #. Replace ``project_template/website/migrations/0001_initial.py`` with
          your newly generated migration.

When making changes that are potentially destructive or backwards incompatible,
increment the minor version number until coderedcms reaches a stable 1.0 release.
Each production project that uses coderedcms should specify the appropriate
version in its requirements.txt to prevent breakage.

.. note::

   When testing existing projects with coderedcms installed from a development
   branch, be sure to use a disposable database, as it is likely that the
   migrations will not be the same migrations that get released.


Branching Strategy
------------------

Primary development takes place in individual branches for each feature or bug.
Changes are then made as a pull request against the ``main`` branch.

The ``main`` branch is the primary working branch, representing the development
version of coderedcms.

Releases are maintained in ``release/X.Y`` branches, where X is the Major
version and Y is the Minor version. Maintenance patches are applied in ``main``
(if applicable) and then merged or cherry-picked into the respective release
branch.


A Note on Cross-Platform Support
--------------------------------

Wagtail CRX works equally well on Windows, macOS, and Linux. When adding new features
or new dependencies, ensure that these utilize proper cross-platform utilities in Python.

To ease local development of Wagtail CRX, we have some automation scripts using
cross-platform `PowerShell Core <https://github.com/powershell/powershell>`_.
Throughout this contributing guide, you will encounter various PowerShell
scripts which provide an easy way of running quality control measures.

Our goal is that users of any platform can develop or host a Wagtail CRX website easily.


CSS Development
---------------

When CSS changes are needed for front-end code (not the wagtail admin), Sass should be used.
Each block, page, snippet, or other component that requires styling should have a dedicated ``.scss``
file created beginning with an underscore in ``coderedcms/static/scss/``. Then import the file
in our main ``crx-front.scss`` file. Then build a human readable and minified version of CSS
from the command prompt as so:

.. code-block:: console

    $ cd coderedcms/static/coderedcms/

    $ # Build human readable CSS, and source map for nicer debugging.
    $ pysassc -g -t expanded scss/crx-front.scss css/crx-front.css

    $ # Build minified CSS.
    $ pysassc -t compressed scss/crx-front.scss css/crx-front.min.css

The generated CSS files must also be committed to version control whenever a sass file is
changed, as they are distributed as part of our package.


JavaScript Development
----------------------

All JavaScript should use ``crx-front.js`` as an entry point, meaning feature
detection should happen in ``crx-front.js`` and then only load secondary scripts and CSS
as needed. This ensures only one single small JavaScript file is required on page load, which
reduces render-blocking resources and page load time.

All JavaScript files produced by CodeRed should contain a license header comment. This standard
license header comment states copyright, ownership, license, and also provides compatibility for
`LibreJS <https://www.gnu.org/software/librejs/free-your-javascript.html>`_.

.. code-block:: text

    /*!
    Wagtail CRX (https://www.coderedcorp.com/cms/)
    Copyright 2018-2023 CodeRed LLC
    License: https://github.com/coderedcorp/coderedcms/blob/main/LICENSE
    @license magnet:?xt=urn:btih:c80d50af7d3db9be66a4d0a86db0286e4fd33292&dn=bsd-3-clause.txt BSD-3-Clause
    */

    ... script code here ...

    /* @license-end */


Upgrading 3rd-Party CSS/JavaScript Libraries
--------------------------------------------

External front-end libraries are included in two places:
* Source or distributables are in ``coderedcms/static/coderedcms/vendor/``.
* Referenced via a CDN in ``coderedcms/static/coderedcms/crx-front.js``.

To upgrade, replace the relevant files or links in these two sources. Then be
sure to change any URLs if applicable within the ``base.html`` template.

If changing SASS sources, be sure to test ``.scss`` files in
``coderedcms/project_template/sass/`` which may require changes.


Testing Wagtail CRX
-------------------

To run the unit tests, run the following command. This will output a unit test
report and code coverage report:

.. code-block:: console

    $ pytest coderedcms/

Or more conveniently, run the PowerShell script, which will also print out the
code coverage percentage in the console:

.. code-block:: console

    $ ./ci/run-tests.ps1

Detailed test coverage reports are now available by opening ``htmlcov/index.html``
in your browser (which is ignored by version control).

To compare your current code coverage against the code coverage of the main
branch (based on latest Azure Pipeline build from main) run:

.. code-block:: console

    $ ./ci/compare-codecov.ps1


Adding New Tests
----------------

Test coverage at the moment is fairly minimal and it is highly recommended that
new features and models include proper unit tests. Any testing infrastructure
(i.e. implementations of abstract models and migrations) needed should be added
to the ``tests`` app in your local copy of Wagtail CRX. The tests themselves
should be in their relevant section in Wagtail CRX (i.e. tests for models in
``coderedcms.models.page_models`` should be located in
``coderedcms.models.tests.test_page_models``).

For example, here is how you would add tests for a new abstract page type,
``CoderedCustomPage`` that would live in ``coderedcms/models/page_models.py``:

#. Navigate to ``coderedcms/tests/testapp/models.py``
#. Add the following import: ``from coderedcms.models.page_models import CoderedCustomPage``
#. Implement a concrete version of ``CoderedCustomPage``, i.e. ``CustomPage(CoderedCustomPage)``.
#. Run ``python manage.py makemigrations`` to make new testing migrations.
#. Navigate to ``coderedcms/models/tests/test_page_models.py``
#. Add the following import: ``from coderedcms.models import CoderedCustomPage``
#. Add the following import: ``from coderedcms.tests.testapp.models import CustomPage``
#. Add the following to the bottom of the file:

   .. code-block:: python

       class CoderedCustomPageTestCase(AbstractPageTestCase, WagtailPageTests):
           model = CoderedCustomPage

#. Add the following to the bottom of the file:

   .. code-block:: python

       class CustomPageTestCase(ConcreteBasicPageTestCase, WagtailPageTests):
           model = CustomPage

#. Write any specific test cases that ``CoderedCustomPage`` and ``CustomPage``
   may require.


Static Analysis
---------------

All code should be formatted with ``black`` before committing:

.. code-block:: console

    $ black .

Flake8 is used to check for syntax and style errors. To analyze the entire
codebase, run:

.. code-block:: console

    $ flake8 .


Contributor Guidelines
----------------------

We are happy to accept pull requests from the community if it aligns with our
vision for coderedcms. When creating a pull request, please make sure you
include the following:

* A description in the pull request of what this change does and how it works.
* Reference to an issue if the change is related to one of the issues on our
  GitHub page.
* Documentation updates in the ``docs/`` directory describing your change.
* Unit tests, or a description of how the change was manually tested.

Following submission of your pull request, a CodeRed member will review and test
your change. **All changes, even by CodeRed members, must go through a pull
request process to ensure quality.**


Merging Pull Requests
---------------------

Follow these guidelines to merge a pull request into the main branch:

* Unit tests pass.
* Code coverage is not lower than main branch.
* Documentation builds, and the PR provides documentation (release notes at a
  minimum).
* If there is a related issue, the issue is referenced and/or closed (if
  applicable)
* Finally, always make a squash merge with a single descriptive commit message.
  Avoid simply using the default commit message generated by GitHub if it is a
  summary of previous commits or is not descriptive of the change.

In the event that the pull request needs more work that the author is unable to
provide, the following process should be followed:

* Create a new branch from main in the form of ``merge/pr-123`` where 123 is
  the original pull request number.
* Edit the pull request to merge into the new branch instead of main.
* Make the necessary changes and submit for review using the normal process.
* When merging this branch into main, follow the same process above, but be
  sure to credit the original author(s) by adding their names to the bottom of
  the commit message as so (see
  `GitHub documentation <https://help.github.com/en/articles/creating-a-commit-with-multiple-authors>`_):

  .. code-block:: text

      Co-authored-by: name <name@example.com>
      Co-authored-by: another-name <another-name@example.com>


Building Python Packages
------------------------

To build a publicly consumable pip package, run:

.. code-block:: console

    $ python setup.py sdist bdist_wheel


Building Documentation
----------------------

For every code or feature change, be sure to update the docs in the repository.
To build the documentation run the PowerShell script, which will also check for
errors in the documentation:

.. code-block:: console

    $ ./ci/make-docs.ps1

Or manually using sphinx:

.. code-block:: console

    $ sphinx-build -M html docs/ docs/_build/ -W

Output will be in ``docs/_build/html/`` directory.

Updating Tutorial Documentation
-------------------------------

From time to time, the documentation for the tutorial will need to be updated. You can work directly in
the tutorial site by loading the fixture file for its database (read more at :ref:`load-data`).

However, once you have worked in the tutorial site and gotten new screenshots for the **Getting Started** documentation,
you will also need to update the fixture file, which is located in ``tutorial > mysite > website > fixtures``.

**These are the steps for updating the fixture:**

1. From the command line, type ``python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > dumpdata.json``

2. The dumped data file will show up in the ``website`` folder. Open it and copy/paste its contents into a new file called ``database.json``. This will fix the encoding issue you would run into otherwise. Save the new fixture file and delete the one that was dumped. Also delete the one that is currently in the ``fixtures`` folder.

3. Move the ``database.json`` file into the ``fixtures`` folder.

4. For testing ``loaddata``, please review the steps at  :ref:`load-data`.


Publishing a New Release
------------------------

.. note::

    For creating pre-releases, use the "rc" version specifier in
    ``coderedcms/__init__.py``. When publishing a production release, leave this
    blank. After a release is completed, increment the version and add the
    "dev0" version specifier.

First checkout the code/branch for release.

Next build a pip package:

.. code-block:: console

    $ python setup.py sdist bdist_wheel

Then upload the pip package to the Python Package Index:

.. code-block:: console

    $ twine upload dist/*

Finally build and update docs:

.. code-block:: console

    $ ./ci/make-docs.ps1

Copy the contents of ``docs/_build/html/`` to the CodeRed docs server under the existing version directory. Using the ``cr`` tool:

.. code-block:: console

   $ cr upload --path ./docs/_build/html/ --remote /www/wagtail-crx/ docs

Note that we do not release separate documentation versions for minor or
maintenance releases. Update the existing major version docs with release notes
and other changes.
