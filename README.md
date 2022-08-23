# Wagtail CRX (CodeRed Extensions)

The professional WordPress alternative for building marketing websites with
Wagtail and Bootstrap.

[Website](https://www.coderedcorp.com/cms/)
|
[Documentation](https://docs.coderedcorp.com/wagtail-crx/)
|
[Blog](https://www.coderedcorp.com/blog/tag/django-wagtail/)


## Status

|                        |                      |
|------------------------|----------------------|
| Python Package         | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/coderedcms)](https://pypi.org/project/coderedcms/) [![PyPI - Django Version](https://img.shields.io/pypi/djversions/coderedcms)](https://pypi.org/project/coderedcms/) [![PyPI - Wheel](https://img.shields.io/pypi/wheel/coderedcms)](https://pypi.org/project/coderedcms/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/coderedcms)](https://pypi.org/project/coderedcms/) [![PyPI](https://img.shields.io/pypi/v/coderedcms)](https://pypi.org/project/coderedcms/) |
| Build                  | [![Build Status](https://dev.azure.com/coderedcorp/cr-github/_apis/build/status/coderedcms?branchName=dev)](https://dev.azure.com/coderedcorp/coderedcms/_build/latest?definitionId=1&branchName=dev) [![Azure DevOps tests (branch)](https://img.shields.io/azure-devops/tests/coderedcorp/cr-github/1/dev)](https://dev.azure.com/coderedcorp/cr-github/_build/latest?definitionId=1&branchName=dev) [![Azure DevOps coverage (branch)](https://img.shields.io/azure-devops/coverage/coderedcorp/cr-github/1/dev)](https://dev.azure.com/coderedcorp/cr-github/_build/latest?definitionId=1&branchName=dev) |


## What is Wagtail CRX?

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


## Quick start

1. Run `pip install coderedcms`

2. Run `coderedcms start mysite --sitename "My Company Inc." --domain www.example.com`

    *Note: `--sitename` and `--domain` are optional to pre-populate settings of your website.*

3. Enter the project `cd mysite/`

4. Run `python manage.py migrate` to create the core models.

5. Run `python manage.py createsuperuser` to create the initial admin user.

6. Run `python manage.py runserver` to launch the development server, and go to `http://localhost:8000` in your browser, or `http://localhost:8000/admin/` to log in with your admin account.

See the [documentation](https://docs.coderedcorp.com/wagtail-crx/) for next steps and customizing your new site.


## Contributors

In addition to the CodeRed team, many thanks to the Wagtail community and our
[independent contributors](https://github.com/coderedcorp/coderedcms/graphs/contributors).

If you're interested in building, developing, or contributing to Wagtail CRX,
check out the [Contributing Guide](https://docs.coderedcorp.com/wagtail-crx/stable/contributing/index.html).


## Attribution

Icon files in `coderedcms/templates/coderedcms/icons/`:

* Were sourced from the Fork Awesome project at
  https://github.com/ForkAwesome/Fork-Awesome.
* Are licensed under the Creative Commons Attribution 3.0 Unported
  license, a copy of which is available at
  https://creativecommons.org/licenses/by/3.0/
* Have been modified from the original sources.


## Contact

We would love to hear your questions, comments, and feedback. Open an issue on Github, message us on [#coderedcms in the Wagtail slack](https://wagtailcms.slack.com/messages/CEU45SBRR).
