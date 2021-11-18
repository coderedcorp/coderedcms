<p align="center">
  <a href="https://www.coderedcorp.com/cms/"><img src="https://www.coderedcorp.com/static/img/cms-hero.png" width="75%" alt=""></a>
</p>
<h3 align="center">Wagtail CRX</h3>
<p align="center">
  The professional WordPress alternative for building marketing websites with
  Wagtail and Bootstrap.
</p>
<p align="center">
  <a href="https://www.coderedcorp.com/cms/">Website</a>
  |
  <a href="https://docs.coderedcorp.com/cms/">Documentation</a>
  |
  <a href="https://www.coderedcorp.com/blog/tag/django-wagtail/">Blog</a>
</p>



## Status

|                        |                      |
|------------------------|----------------------|
| Python Package         | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/coderedcms)](https://pypi.org/project/coderedcms/) [![PyPI - Django Version](https://img.shields.io/pypi/djversions/coderedcms)](https://pypi.org/project/coderedcms/) [![PyPI - Wheel](https://img.shields.io/pypi/wheel/coderedcms)](https://pypi.org/project/coderedcms/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/coderedcms)](https://pypi.org/project/coderedcms/) [![PyPI](https://img.shields.io/pypi/v/coderedcms)](https://pypi.org/project/coderedcms/) |
| Build                  | [![Build Status](https://dev.azure.com/coderedcorp/cr-github/_apis/build/status/coderedcms?branchName=dev)](https://dev.azure.com/coderedcorp/coderedcms/_build/latest?definitionId=1&branchName=dev) [![Azure DevOps tests (branch)](https://img.shields.io/azure-devops/tests/coderedcorp/cr-github/1/dev)](https://dev.azure.com/coderedcorp/cr-github/_build/latest?definitionId=1&branchName=dev) [![Azure DevOps coverage (branch)](https://img.shields.io/azure-devops/coverage/coderedcorp/cr-github/1/dev)](https://dev.azure.com/coderedcorp/cr-github/_build/latest?definitionId=1&branchName=dev) |


## What is Wagtail CRX?

Formerly known as CodeRed CMS, Wagtail CRX (CodeRed Extensions),
provides a large set of enhancements and pre-built components for Wagtail which
are ready to use out-of-the box! This saves development time and avoids
"re-inventing the wheel" by providing features commonly needed by websites:

* Streamfield blocks and templates for Bootstrap 4: rows, columns, hero units,
  carousels, buttons, modals, cards, and more!

* Settings for adding logo, navigation, footer, and other common elements.

* Rich set of SEO tagging attributes on each page.

* Configurable Google Analytics tracking.

* Robust form builder including the ability for multi-step forms, conditional
  logic, customized confirmation emails, MailChimp integration, and more (all
  from within the streamfield!)

* Article pages for building blogs, news, etc.

* Calendar and event pages.

* Google Maps blocks, and store locator functionality.

* Dynamic classifier system, for creating filterable categories.

* Website search functionality, filterable by page type.

* Style your site using SASS/SCSS directly from Django, without the need for
  Node.js


## Quick start

1. Run `pip install coderedcms`

2. Run `coderedcms start mysite --sitename "My Company Inc." --domain www.example.com`

    *Note: `--sitename` and `--domain` are optional to pre-populate settings of your website.*

3. Enter the project `cd mysite/`

4. Run `python manage.py migrate` to create the core models.

5. Run `python manage.py createsuperuser` to create the initial admin user.

6. Run `python manage.py runserver` to launch the development server, and go to `http://localhost:8000` in your browser, or `http://localhost:8000/admin/` to log in with your admin account.

See the [documentation](https://docs.coderedcorp.com/cms/) for next steps and customizing your new site.


## Inspiration and Design Philosophy

### Inspiration from WordPress

We the creators of Wagtail CRX deal with WordPress sites on a daily basis. While WordPress is fantastic for blogs and do-it-yourself websites, we feel it is very frustrating for use in a professional environment where the site needs to be actively enhanced, maintained, and secured on a daily basis. We designed Wagtail CRX as a marketing-focused WordPress replacement, *not* a WordPress clone. The intended audience is an agency, technology firm, business, or non-profit who has at least one full stack web developer managing the website.

WordPress users will feel comfortable with the CodeRed Extensions, as many of the editing and design paradigms are similar such as:

* Global site and branding settings.

* Main menu builder is familiar.

* Editors can change the template used by each page.

PLUS many aspects are greatly enhanced:

* Visual content blocks eliminate need for cryptic short-codes.

* Content blocks can each be customized with CSS classes and selectable templates.

* Developers can easily customize the editing interface and page types without 3rd party plugins or themes.

* The site can be professionally managed with better control over 3rd party plugins to prevent unplanned breakage (if you've ever managed a large WordPress site - you know exactly how painful this is).

### As an Extension of Wagtail

Wagtail CRX is a pip package that essentially wraps Wagtail and provides marketing-specific features that are ready to be used out of the box. Everything that can be done with Wagtail can be done with CRX.

One major point of difference between between CodeRed and stock Wagtail is the approach to design and content. Wagtail being more of a CMS framework, is focused on a clear separation between design (UX) and content. We agree with this approach for larger informational sites. But as is usually the case with marketing sites, design and information are more tightly coupled. Developers shouldn’t *need* to create a new page type or a new block just to handle a design deviation that is used in one place on the site. Designers and editors shouldn’t *need* to engage the developer for every minor design-related change such as changing a CSS class. For this reason, CodeRed blurs the lines of design and content by enabling editors to specify templates on a per-page and per-block basis, CSS classes per-block, and many other logo, layout, and branding settings. We realize this is not the right approach for every site - but we do believe it adds a lot of value for marketing sites.


## Contributors

In addition to the CodeRed team, many thanks to the Wagtail community and our
[independent contributors](https://github.com/coderedcorp/coderedcms/graphs/contributors).

If you're interested in building, developing, or contributing to Wagtail CRX,
check out the [Contributing Guide](https://docs.coderedcorp.com/cms/stable/contributing/index.html).


## Contact

We would love to hear your questions, comments, and feedback. Open an issue on Github, message us on [#coderedcms in the Wagtail slack](https://wagtailcms.slack.com/messages/CEU45SBRR).
