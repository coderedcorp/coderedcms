Customize Navbar and Footer
===========================

Navbar
------

The navbar (also known as Navigation Bar, Header, or Menu) is a shared piece
navigation. Wagtail CRX shows an area for the navbar at the top of most pages on
the site. The logo and style of the navbar can be customized under **Settings >
Layout**. The links shown in the navbar can be customized by creating a "Navbar"
snippet under **Snippets > Navbar**.

.. note::

    Each Navbar snippet is rendered sequentially in the navbar area. This currently
    does not support multi-site, i.e. all Navbar snippets are present on all sites.

Customizing the design of the stock navbar can be accomplished by baked in
Django template overrides.

Create a ``templates\coderedcms\snippets`` directory in your project,
most likely in the ``website`` directory.

In that directory create a file called ``navbar.html``. This file will then
override the ``navbar.html`` file included with Wagtail CRX.

It is advisable to initially copy the contents of `Wagtail CRX navbar.html`_, but
not necessary.

.. _Wagtail CRX navbar.html: https://github.com/coderedcorp/coderedcms/blob/main/coderedcms/templates/coderedcms/snippets/navbar.html


Footer
------

The footer is a shared piece of content shown at the bottom of every page on the
site. Content can be added to the footer by creating a "Footer" snippet under
**Snippets > Footer**.

.. note::

    Each Footer snippet is rendered sequentially in the footer area. This
    currently does not support multi-site, i.e. all Footer snippets are present
    on all sites.

Customizing the design of the sock footer can be accomplished similarly to the
navbar, by overriding the Django template.

Create a ``templates/coderedcms/snippets/`` directory in your project,
most likely in the ``website`` directory.

In that directory create a filed named ``footer.html``. This file will then
override the ``footer.html`` file included with Wagtail CRX.

Similarly, it is advisable to initially copy the contents of `Wagtail CRX
footer.html`_, but not necessary.

.. note::

    You can now create more than one navbar menu or footer and choose which ones to render on your site. In **Settings > CRX Settings**,
    select your navbars in **Site Navbars**. Select your footers in **Site Footers**. The Site Navbar Layout includes settings for the whole
    navbar, while the Site Navbar chooser allows you to choose which menu you want for your site. This features allows you to
    select a different navbar/footer per site in a multisite installation OR render several navbars/footers in selected order
    on a single site.

.. _Wagtail CRX footer.html: https://github.com/coderedcorp/coderedcms/blob/main/coderedcms/templates/coderedcms/snippets/footer.html
