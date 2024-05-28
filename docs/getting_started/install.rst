.. _installation:

Installation
============

.. note::
     The tutorial uses the pro template. We recommend all serious websites start with the pro template for best flexibility:
     :ref:`sass_install`


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


#. In your virtual environment, install CRX:

   .. code-block:: console

      $ pip install coderedcms

#. Create a new project:

   .. code-block:: console

      $ coderedcms start mysite --sitename "My Company Inc." --domain "www.example.com"

   *``--sitename`` and ``--domain`` are optional to pre-populate settings of your website.*

#. Next, enter the new project folder and set up Django.

   .. code-block:: console

      $ python manage.py migrate
      $ python manage.py createsuperuser

#. Now, you can run a local development server:

   .. code-block:: console

      $ python manage.py runserver

   Go to http://localhost:8000 in your browser, or http://localhost:8000/admin/ to log in with your admin account.

✨🎉 You now have Wagtail CRX up and running! 🎉✨

.. _sass_install:

Professional Installation
-------------------------

The professional boilerplate includes additional features pre-configured, such as:

* Custom Image and Document models.
* Custom User model (using email address as username).
* Custom Navbar and Footer.
* SCSS compilation (using Python, not Node.js).
* Ruff, MyPy, Pytest tooling pre-configured.

To use the professional boilerplate, add ``--template pro`` to the start command:

#. In your virtual environment, install CRX:

   .. code-block:: console

      $ pip install coderedcms

#. Create a new project:

   .. code-block:: console

      $ coderedcms start mysite --template pro --sitename "My Company Inc." --domain "www.example.com"

   *``--sitename`` and ``--domain`` are optional to pre-populate settings of your website.*

#. Next, enter the new project folder:

   .. code-block:: console

      $ cd mysite/

#. Install the development tooling with:

   .. code-block:: console

      $ pip install -r requirements-dev.txt

#. Next, set up Django.

   .. code-block:: console

      $ python manage.py migrate
      $ python manage.py createsuperuser

#. Compile the scss code into CSS:

   .. code-block:: console

       $ python manage.py sass website/static/website/src/custom.scss website/static/website/css/custom.css

   .. note::
       To build the Sass automatically whenever you change a file, add the
       ``--watch`` option and run it in a separate terminal. For more options,
       see `django-sass <https://github.com/coderedcorp/django-sass/>`_.

#. Now, you can run a local development server:

   .. code-block:: console

      $ python manage.py runserver

   Go to http://localhost:8000 in your browser, or http://localhost:8000/admin/ to log in with your admin account.

When working with Sass, you will want to look at the base.html file provided at:
``mysite/website/templates/coderedcms/pages/base.html`` to load in any custom
CSS or JavaScript as needed.

Follow the tutorial to build a website with us: :doc:`tutorial01`.

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
|            | SCSS to CSS compilation. Custom Navbar and Footer. Developer    |
|            | tooling such as ruff, mypy, and pytest.                         |
+------------+-----------------------------------------------------------------+

.. versionchanged:: 3.0

   The "pro" template was added in version 3.0. Previously it was named "sass" and had fewer features.
