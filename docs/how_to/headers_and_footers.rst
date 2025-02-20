Customize Navbar and Footer
===========================

Navbar
------
The navbar (also known as Navigation Bar, Header, or Menu) is a shared piece of
navigation. Wagtail CRX shows an area for the navbar at the top of most pages on
the site. The logo and style of the navbar can be customized under **Settings >
Layout**.

For the basic template, create and manage navbars under **Snippets > Navbar**. Then use
**Settings > CRX Settings** to select which navbars to display and their ordering. The
Site Navbar Layout includes settings for the whole navbar, while the Site Navbar chooser
allows you to select specific navbars for your site.

For the pro template, create navbars under **Snippets > Navbar** and select the specific
site for each navbar within the navbar snippet edit page. Navbars are ordered by the
default model ordering. When no site-specific navbars are configured and
`CRX_NO_SITE_NAVBAR_FALLBACK` is True (default in pro template), all navbars will be
displayed. Set `CRX_NO_SITE_NAVBAR_FALLBACK = False` in your settings to disable this
fallback behavior.

Customizing the design of the stock navbar can be accomplished through Django template
overrides. Create a `templates/coderedcms/snippets` directory in your project,
most likely in the `website` directory.

In that directory create a file called `navbar.html`. This file will then
override the `navbar.html` file included with Wagtail CRX.

It is advisable to initially copy the contents of [Wagtail CRX navbar.html](https://github.com/coderedcorp/coderedcms/blob/main/coderedcms/templates/coderedcms/snippets/navbar.html), but
not necessary.

Footer
------
The footer is a shared piece of content shown at the bottom of every page on the
site. Create footers under **Snippets > Footer**.

For the basic template, use **Settings > CRX Settings** to select which footers to
display and specify their ordering through the Site Footers setting.

For the pro template, select the specific site within each footer snippet edit page.
Footers are ordered by the default model ordering. When no site-specific footers are
configured and `CRX_NO_SITE_FOOTER_FALLBACK` is True (default in pro template), all
footers will be displayed. Set `CRX_NO_SITE_FOOTER_FALLBACK = False` in your settings
to disable this fallback behavior.

Customizing the design of the stock footer can be accomplished similarly to the
navbar, by overriding the Django template. Create a `templates/coderedcms/snippets/`
directory in your project, most likely in the `website` directory.

In that directory create a file named `footer.html`. This file will then
override the `footer.html` file included with Wagtail CRX.

Similarly, it is advisable to initially copy the contents of [Wagtail CRX
footer.html](https://github.com/coderedcorp/coderedcms/blob/main/coderedcms/templates/coderedcms/snippets/footer.html), but
not necessary.
