.. _installation:

Installation
============

.. note::
     The tutorial uses Sass Support. It is recommended to use sass to follow along with the tutorial.  See:
     :ref:`sass_install`


Basic Installation
------------------

#. Make a directory (folder) for your project.
#. Create a virtual environment.
    **Not sure how to create a virtual environment?**
    Creating a virtual environment for your project only involves a few commands.
    See below:

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

.. _sass_install:

Installing with Sass Support
----------------------------

To create a project that is pre-configured to use Sass for CSS compilation:

#. Run ``pip install coderedcms``
#. Run

   .. code-block:: console

       $ coderedcms start mysite --template sass --sitename "My Company Inc." --domain www.example.com

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

Follow the tutorial to build a website with us: :doc:`tutorial01`.

Starter Templates
-----------------

You can start a new Wagtail CRX project with a custom template directory available on
or at a URL using the ``--template`` option. Additionally, we provide some built-in templates:

+------------+-------------------------------------------------------------------+
| Template   | Description                                                       |
+============+===================================================================+
| ``basic``  | The simplest option, good for many sites.                         |
|            |                                                                   |
+------------+-------------------------------------------------------------------+
| ``sass``   | Similar to basic, but with extra tooling to support SCSS to CSS   |
|            | compilation. Used in the tutorial                                 |
+------------+-------------------------------------------------------------------+
