Customize the design of your website
====================================

Below are a few settings that can be used to change branding, design, and layout of your website.

Site name
---------

This is shown by default in the navbar, and also added to the title attribute of each page.
This can be changed in Settings > Sites > localhost. Hostname and port only need to be changed
when running in  production.

:ref:`site-name`

Site settings
-------------

Under Settings > Sites in the Wagtail Admin, you will want to make sure this setting is up
to date with the proper Hostname and Port. Failure to do so can cause the Preview button on
pages to return a 500 error.

Logo & icon
-----------

The logo that appears in the navbar, the wagtail admin, and your favicon can be set in
Settings > CRX Settings. Here you can also change navbar settings (based on Bootstrap CSS framework).

:ref:`logo`

Menu / navigation bars
----------------------

Navbars are top navigation elements that create a "main menu" experience. Navbars are managed
as snippets. They render from top down based on the order they were created in.

:ref:`navbar-global`

:ref:`navbar`

Footers
-------

Similar to Navbars, footers are also managed as snippets and also render top down based on
the order they were created in.

:ref:`footer`

Custom CSS
----------

A Django app called ``website`` has been created to hold your custom changes. In website/static/
there are custom.css and custom.js files that get loaded on every page by default. Adding
anything to these files will automatically populate on the site and override any default styles.
By default, Bootstrap 5 is already included on the site.

.. note::
    You can also use Bootstrap color and utility classes in the **Custom CSS** fields on your pages in CMS.
    Sometimes you may need more customization than Bootstrap classes can provide, in which case you can
    create your own custom classes in your CSS files and use them in your templates and in the CMS.

Custom HTML templates
---------------------

To learn how to create custom HTML templates, see the advanced tutorial:
:doc:`/advanced/advanced01`.
