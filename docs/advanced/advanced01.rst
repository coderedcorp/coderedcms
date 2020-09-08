Advanced: Customizing HTML/CSS in Templates
===========================================

Overview
---------
CodeRed CMS is an extension of Wagtail CMS. You can further customize your site by overriding the 
built-in templates to suit your needs. For this tutorial, we will assume that you have basic knowledge 
of the Django templating language. You can read more about it by visiting
`Django template language <https://docs.djangoproject.com/en/3.0/ref/templates/language/>`_.

The templating language uses a series of ``{%  %}`` to pull in content from your page models (found in 
the models.py file) and add minimal logic to the page. This allows it to render the page after content 
is added in the CMS and allows you to create multiple pages with the same layout. At the top of the page,
you also want to make sure to either specify that you are **extending a page template** and that you are 
pulling in Wagtail tags to make your template work the way it should. 

.. note::
    If you are completely overriding a template, you will not use the ``{% extends "path/to/template" %}`` 
    at the top of your template. You do, however, need to make sure to use the appropriate Wagtail 
    tags at the top of the template or your template will not render.

Example 1: Navbar Customization
-------------------------------

The built-in template for the navbar can be found in ``templates/coderedcms/snippets/navbar.html``. This 
file may not actually be in your installation folders for your site; however, you can see its contents 
by visiting the GitHub page for the code here: `Snippets – Navbar <https://github.com/coderedcorp/coderedcms/blob/dev/coderedcms/templates/coderedcms/snippets/navbar.html>`_. 

Let’s say that you want to have a 2-tiered navbar with the logo on the top tier and the menu items on the
second tier. The default navbar does not have that as an option, so you will want to override this template. 

Look at your folder structure for your project. In the ``website`` folder, you should see another folder 
called ``templates``. In there are two folders as well: ``website`` and ``coderedcms``. The ``coderedcms`` template 
folder is likely empty at this point because the CMS is pulling in the default templates from source, but you can 
add templates to the ``coderedcms`` folder **if you are overriding the default templates**.

Most of your custom templates will go into your ``website`` folder because they are not overriding the 
default templates in the CMS but either extending them or creating completely new ones specific to 
your site. 

.. note::
    Adding templates to the ``coderedcms`` templates folder does not change the default templates 
    throughout all of CodeRed CMS but does override those specific templates for your website app.

Your ``website`` folder currently only has a folder for ``coderedcms`` in the ``templates`` folder. 
You can add a new ``website`` folder in ``templates`` (because we will use it in another tutorial), 
but for now, you will want to add a ``snippets`` folder inside the ``templates\coderedcms`` folder 
so that your folder structure looks something like this:

.. figure:: img/advanced_folder_structure1.png
    :alt: Our folder structure for templates.

    Our folder structure for templates within our website app.

