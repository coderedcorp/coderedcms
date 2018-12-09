Customize the design of your website
====================================

After installation, you are greeted by a barebones website.
There are a few settings you will want to change to add your own branding.

Site name
---------

This is shown by default in the navbar, and also added to the title attribute of each page.
This can be changed in Settings > Sites > localhost. Hostname and port only need to be changed
when running in  production.

Site settings
-------------

Under Settings > Sites in the Wagtail Admin, you will want to make sure this setting is up
to date with the proper Hostname and Port. Failure to do so can cause the Preview button on
pages to return a 500 error.

Logo & icon
-----------

The logo that appears in the navbar, the wagtail admin, and your favicon can be set in
Settings > Layout. Here you can also change navbar settings (based on Bootstrap CSS framework).

Menu / navigation bars
----------------------

Navbars are top navigation elements that create a "main menu" experience. Navbars are managed
as snippets. They render from top down based on the order they were created in.

Footers
-------

Similar to Navbars, footers are also managed as snippets and also render top down based on
the order they were created in.

Custom CSS
----------

A django app called ``website`` has been created to hold your custom changes. In website/static/
there are custom.css and custom.js files that get loaded on every page by default. Adding
anything to these files will automatically populate on the site and override any default styles.
By default, Bootstrap 4 and jQuery are already included on the site.

Custom HTML templates
---------------------

The templates directory inside the ``website`` app is empty by default. Any templates you put
in here will override the default coderedcms templates if they follow the same name and directory
structure. This uses the standard Django template rendering engine. For example, to change the
formatting of the article page, copy ``coderedcms/templates/coderedcms/pages/article_page.html``
to ``website/templates/coderedcms/pages/article_page.html`` and modify it.
