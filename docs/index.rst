Wagtail CRX (CodeRed Extensions)
================================

`Official website <https://www.coderedcorp.com/cms/>`_ | `Source code on GitHub <https://github.com/coderedcorp/coderedcms>`_

CRX, formerly known as CodeRed CMS, provides a large set of enhancements and
pre-built components for Wagtail which are ready to use out-of-the box! This
saves development time and avoids "re-inventing the wheel" by providing features
commonly needed by websites:

* Streamfield blocks and page templates for Bootstrap 5: rows, columns, hero
  units, carousels, buttons, modals, cards, and more!

* Settings for adding logo, navigation, footer, and other common elements.

* Rich set of SEO tagging attributes on each page.

* Configurable Google Analytics and other tracking.

* Robust form builder including the ability for multi-step forms, conditional
  logic, customized confirmation emails, MailChimp integration, and more.

* Article pages for building blogs, news, etc.

* Calendar and event pages.

* Google Maps blocks, and store locator functionality.

* Dynamic classifier system, for creating filterable categories.

* Website search functionality, filterable by page type.

* Style your site using SASS/SCSS directly from Django, without the need for
  Node.js


Wagtail CRX is "just" Wagtail
-----------------------------

An important line of distinction is that Wagtail CRX is not a fork of Wagtail,
or a competing version of Wagtail. It is simply a pip package which provides
additional features on top of stock Wagtail you know and love.

CRX is to Wagtail, what Wagtail is to Django. A set of additional features for
web developers to save time and turn out high-quality websites. CRX is not a
drag-n-drop or no-code solution (although many of the features do not require
coding).

Our motivation for making Wagtail CRX is to enable a developer to quickly build
a Wagtail website by pulling in pre-built components which have been heavily
tested and are guaranteed to work in a consistent way. This is why the project
is tightly coupled with Bootstrap CSS. This is a boon for web development teams:
rather than copy-pasting code from one project to the next, code is centralized
in a generic way in CRX and can be reused by many sites. This also helps
with maintenance and Wagtail upgrades --- bugs and upgrades can generally be
implemented once in CRX then pushed out to all sites.


Join us
-------

Have questions or ideas? Join us in the **#coderedcms** channel on the
`Wagtail Slack <https://wagtail.io/slack/>`_.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   getting_started/index
   advanced/index
   features/index
   how_to/index
   reference/index
   contributing/index
   releases/index
