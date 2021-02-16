<p align="center">
  <a href="https://www.coderedcorp.com/cms/"><img src="https://www.coderedcorp.com/static/img/cms-hero.png" width="75%" alt=""></a>
</p>
<h3 align="center">CodeRed CMS</h3>
<p align="center">
  The professional WordPress alternative for building modern marketing websites. Based on Python, Django, Wagtail, and Bootstrap 4.
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



## Note

**This project is still early on in its development lifecycle.** It is possible for breaking changes to occur between versions until reaching a stable 1.0, however we will clearly note any breaking changes between releases if applicable. Feedback and pull requests are welcome.

## Quick start
1. Run `pip install coderedcms`

2. Run `coderedcms start mysite --sitename "My Company Inc." --domain www.example.com`

    *Note: `--sitename` and `--domain` are optional to pre-populate settings of your website.*

3. Enter the project `cd mysite/`

4. Run `python manage.py migrate` to create the core models.

5. Run `python manage.py createsuperuser` to create the initial admin user.

6. Run `python manage.py runserver` to launch the development server, and go to `http://localhost:8000` in your browser, or `http://localhost:8000/admin/` to log in with your admin account.

See the [documentation](https://docs.coderedcorp.com/cms/) for next steps and customizing your new site.



## Why use CodeRed CMS?

In addition to the numerous benefits of [Wagtail](https://wagtail.io/features/), CodeRed has features that are *specifically designed* for marketing websites:

* **The editing experience is tailored for visual marketing content.** Create flashy hero units, callouts, and forms using a beautiful editing interface. Editors and Designers can easily update content, designs, and layout without fear of breakage and without the need to consult developers. Developers can fully customize the site using plain HTML/CSS/JavaScript without relying on plugins or undocumented hacks.

* **Built-in SEO** Optimized metadata for Facebook, Twitter, LinkedIn, Google, Bing, and more are all included out of the box. A sitemap and robots.txt are also present and automatically updated. Articles, blog posts, and events support Google’s preferred AMP format to boost search ranking and support mobile devices.

* **Responsive design** out of the box! Editors can build content using [Bootstrap 4](https://getbootstrap.com/) components including navbars, hero units, carousels, cards, modals, and the powerful grid system.

* **Fast load times** made possible by a built-in page cache. The cache automatically refreshes whenever a page is published, or by the click of a button. Cached pages load as quickly as static HTML files.

* **Full Google Analytics tracking** can be turned on by adding your UA- tag. Detailed event tracking can be turned on globally and fine-tuned for each clickable element such as links, buttons, and images.

* **Professionally-backed support**. Both CodeRed CMS and Wagtail (the technology powering CodeRed CMS) are produced by software companies who offer professional support and services. This is built on proven technology that successfully serves small businesses and large enterprises around the world every day.



## Quality Control

In addition to manual testing by real humans between releases, we also employ many quality control tools to automatically catch some errors before they are introduced to the code. The CodeRed team has a strong focus on quality and security to ensure CodeRed CMS remains reliable for use in day-to-day business operations.



## Roadmap

Officially, CodeRed CMS is in a beta stage. That being said, it is currently in use on production sites. However there are still many activities that are needed before hitting a 1.0 “stable” status.

Work already in progress before 1.0 release:

* Higher test coverage.

* Full documentation.

* Usability feedback and testing regarding the admin/editor experience.

* Improved accessibility of the CodeRed-provided HTML templates (excluding the admin interface... this is an issue wagtail is dealing with upstream).

Other future plans:

* Continue adding commonly used abstract page types and blocks available out of the box(e.g. calendar/events, product page, store locator, etc.)

* Continue updating and enhancing SEO/meta attributes as standards evolve.

* Built-in SSO with major identity providers such as Google and Office 365.

* ADA compliance enforcement features and workflows in the admin.

* Light e-commerce functionality, or at least a smooth integration with an existing e-commerce framework.



## Inspiration and Design Philosophy

### Inspiration from WordPress

We the creators of CodeRed CMS deal with WordPress sites on a daily basis. While WordPress is fantastic for blogs and do-it-yourself websites, we feel it is very frustrating for use in a professional environment where the site needs to be actively enhanced, maintained, and secured on a daily basis. We designed CodeRed CMS as a marketing-focused WordPress replacement, *not* a WordPress clone. The intended audience is an agency, technology firm, business, or non-profit who has at least one full stack web developer managing the website.

WordPress users will feel comfortable with CodeRed CMS, as many of the editing and design paradigms are similar such as:

* Global site and branding settings.

* Main menu builder is familiar.

* Editors can change the template used by each page.

PLUS many aspects are greatly enhanced:

* Visual content blocks eliminate need for cryptic short-codes.

* Content blocks can each be customized with CSS classes and selectable templates.

* Developers can easily customize the editing interface and page types without 3rd party plugins or themes.

* The site can be professionally managed with better control over 3rd party plugins to prevent unplanned breakage (if you've ever managed a large WordPress site - you know exactly how painful this is).

### As an Extension of Wagtail

CodeRed CMS is a pip package that essentially wraps Wagtail and provides marketing-specific features that are ready to be used out of the box. Everything that can be done with Wagtail can be done with CodeRed.

One major point of difference between between CodeRed and stock Wagtail is the approach to design and content. Wagtail being more of a CMS framework, is focused on a clear separation between design (UX) and content. We agree with this approach for larger informational sites. But as is usually the case with marketing sites, design and information are more tightly coupled. Developers shouldn’t *need* to create a new page type or a new block just to handle a design deviation that is used in one place on the site. Designers and editors shouldn’t *need* to engage the developer for every minor design-related change such as changing a CSS class. For this reason, CodeRed blurs the lines of design and content by enabling editors to specify templates on a per-page and per-block basis, CSS classes per-block, and many other logo, layout, and branding settings. We realize this is not the right approach for every site - but we do believe it adds a lot of value for marketing sites.



## Contributors

In addition to the CodeRed team, many thanks to the Wagtail community and our
[independent contributors](https://github.com/coderedcorp/coderedcms/graphs/contributors).

If you're interested in building, developing, or contributing to CodeRed CMS,
check out the [Contributing Guide](https://docs.coderedcorp.com/cms/stable/contributing/index.html).



## Contact

We would love to hear your questions, comments, and feedback. Open an issue on Github, message us on [#coderedcms in the Wagtail slack](https://wagtailcms.slack.com/messages/CEU45SBRR), or email us at info@coderedcorp.com.
