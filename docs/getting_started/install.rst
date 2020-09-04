Installation
============


Basic Installation
------------------

#. Make a directory (folder) for your project.
#. Create a virtual environment. 
    **Not sure how to create a virtual environment?**
    Creating a virtual environment for your project only involves a few commands.
    If you're on a Windows machine, you would run something like the following:

    .. code-block:: console

        $ python -m venv C:\Users\YourComputer\env\name_of_virtual_environment

    You can name your virtual environment anything you like. It is just for your use
    on your computer. 

    Learn more about virtual environments by visiting the `Python documentation on virtual
    environments here <https://docs.python.org/3/tutorial/venv.html>`_.

    .. note::
        You will need to be in the directory (folder) of your CodeRed CMS project and have your
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

✨🎉 You now have CodeRed CMS up and running! 🎉✨

Follow the tutorial to build :doc:`tutorial01`


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

       $ python manage.py sass website/static/website/src/custom.scss website/static/website/css/

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


Starter Templates
-----------------

You can start a new CodeRed CMS project with a custom template directory available on
or at a URL using the ``--template`` option. Additionally, we provide some built-in templates:

+------------+-----------------------------------------------------------------+
| Template   | Description                                                     |
+============+=================================================================+
| ``basic``  | The default CodeRed CMS starter project. The simplest option,   |
|            | good for most sites.                                            |
+------------+-----------------------------------------------------------------+
| ``sass``   | Similar to basic, but with extra tooling to support SCSS to CSS |
|            | compilation.                                                    |
+------------+-----------------------------------------------------------------+
