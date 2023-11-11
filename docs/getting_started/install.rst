Installation
============


Basic Installation
------------------

#. Make a directory (folder) for your project.
#. Create a virtual environment.

    **Windows (PowerShell):**

    .. code-block:: ps1con

       PS> python -m venv .\venv\
       PS> .\venv\Scripts\Activate.ps1

    **macOS, Linux:**

    .. code-block:: console

       $ python -m venv ./venv/
       $ source ./venv/bin/activate

    You can name your virtual environment anything you like. It is just for your use
    on your computer.

    Learn more about virtual environments by visiting the `Python documentation on virtual
    environments here <https://docs.python.org/3/tutorial/venv.html>`_.

    .. note::

       You will need to be in the directory (folder) of your Wagtail project and have your
       virtual environment activated to install dependencies and run your site.

#. Run ``pip install coderedcms``
#. Run ``coderedcms start mysite --sitename "My Company Inc." --domain www.example.com``

   .. note::
       ``--sitename`` and ``--domain`` are optional to pre-populate settings of your website.

#. Enter the ``mysite`` project with ``cd mysite/``.
#. Run ``python manage.py migrate`` to create the core models.
#. Run ``python manage.py createsuperuser`` to create the initial admin user.
#. Run ``python manage.py runserver`` to launch the development server, and go to
   http://localhost:8000 in your browser, or http://localhost:8000/admin/ to log in
   with your admin account.

✨🎉 You now have Wagtail CRX up and running! 🎉✨

Follow the tutorial to build: :doc:`tutorial01`.

You can also play around with our tutorial database. Learn more: :ref:`load-data`.


Professional Installation (includes Sass/SCSS)
----------------------------------------------

The professional boilerplate includes additional features pre-configured, such as:

* Custom Image and Document models
* Custom User model (using email address as username)
* SCSS compilation (using Python, not Node.js)
* Ruff, MyPy, Pytest tooling pre-configured

To use the professional boilerplate, add ``--template pro`` to the start command:

#. Run ``pip install coderedcms``
#. Run

   .. code-block:: console

      $ coderedcms start mysite --template pro --sitename "My Company Inc." --domain www.example.com

   .. note::

      ``--sitename`` and ``--domain`` are optional to pre-populate settings of your website.

#. Enter the ``mysite`` project with ``cd mysite/``.
#. Install the development tooling with:

   .. code-block:: console

       $ pip install -r requirements.txt -r requirements-dev.txt

#. Run ``python manage.py migrate`` to create the core models.
#. Run ``python manage.py createsuperuser`` to create the initial admin user.
#. Compile the scss code into CSS:

   .. code-block:: console

       $ python manage.py sass website/static/website/src/custom.scss website/static/website/css/custom.css

   .. note::
       To build the Sass automatically whenever you change a file, add the
       ``--watch`` option and run it in a separate terminal. For more options,
       see `django-sass <https://github.com/coderedcorp/django-sass/>`_.

#. Run ``python manage.py runserver`` to launch the development server, and go to
   http://localhost:8000 in your browser, or http://localhost:8000/admin/ to log in
   with your admin account.

When working with Sass, you will want to look at the base.html file provided at:
``mysite/website/templates/coderedcms/pages/base.html`` to load in any custom
CSS or JavaScript as needed.

.. _load-data:

Adding Our Tutorial Database
----------------------------

You can follow along with our tutorial and upload your own pictures and content; however,
we have included our database data from our tutorial project so you can take a tour inside of
the project and play around with it. The database is located in ``website > fixtures > database.json``.

Follow these steps to upload it:

1. Navigate to the tutorial project in the Command Line by going to ``coderedcms > tutorial > mysite``.

2. In a fresh virtual environment, type ``pip install -r requirements.txt`` to set up the requirements for the project.

3. Set up your database like usual. If you want to use a database other than the default ``sqlite3``, you will need to set it up first. It will be an empty database for now.

4. Do the initial migration for the tutorial site with ``python manage.py migrate``.

5. Navigate to the ``database.json`` file in the Fixtures folder and copy the path to the file.

6. From the Command Line, type ``python manage.py loaddata "path/to/database.json"``, replacing that last part with the correct path to the file.

7. Check to see if it worked by running ``python manage.py runserver``. You should now see our tutorial project with all of the content we have added to the site. It's ready for you to play around with it!


Starter Templates
-----------------

You can start a new Wagtail CRX project with a custom template directory available on
or at a URL using the ``--template`` option. Additionally, we provide some built-in templates:

+------------+-----------------------------------------------------------------+
| Template   | Description                                                     |
+============+=================================================================+
| ``basic``  | The default starter project. The simplest option, good for most |
|            | sites.                                                          |
+------------+-----------------------------------------------------------------+
| ``pro``    | Custom Image, Document, User models. Extra tooling to support   |
|            | SCSS to CSS compilation. Developer tooling such as ruff, mypy,  |
|            | and pytest.                                                     |
+------------+-----------------------------------------------------------------+

.. versionchanged:: 3.0

   The "pro" template was added in version 3.0. Previously it was named "sass" and had fewer features.
