Web Pages
===================

The standard page for your website.  All other page types on the site will share the functionality of this page type.

Usage
-----

First start by creating a "Web Page".  Each page on your site will have an assortment of tabs that house different types of data/content for that page.


Content Tab
~~~~~~~~~~~

The **Content** tab is meant to house all data fields related to the page's content.  You have the following options:

* **Title**: The name of the page.
* **Cover Image**: The big hero image you want for the page.
* **Body**: The field your content will live.  This uses a StreamField to allow you to dynamically create a page layout and content.

Classify Tab
~~~~~~~~~~~~

The **Classify** tab is meant to house all data fields related to the page's classification.  You have the following options:

* **Classifier Terms**: The taxonomies you want assigned to this page.  These taxonomies can be used for certain blocks to control what pages are related to a certain block.  These taxonomies are defined in the Snippets section of the admin.
* **Tags**: An optional tagging mechanism that can be used by a developer for any reason.

Layout Tab
~~~~~~~~~~

The **Layout** tab is meant to house all data fields related to the page's layout.  You have the following options:

* **Template**:  The template you want the page to use to render.
* **Show List of Child Pages**: Toggles whether this parent page should show a list of it's children pages.
* **Number Per Page**: Controls how many children pages you want to show at once.
* **Order Children Pages by**: Controls how the children pages are sorted on this parent page.
* **Filter Child Pages by**: Using Classifier terms, control which children pages are shown on the parent page.

SEO Tab
~~~~~~~

The **SEO** tab is meant to house all data fields related to the page's SEO  settings, like Open Graph tags and Google's structured data.  You have the following options:

* **Slug**: The url path you want the page to exist on.  If not set, it will be automatically generated from this page's title.
* **Page Title**: The title you want to be shown at the top of your web browser
* **Search Description**: The description you want to be placed in your site's meta tags.
* **Open Graph preview image**:  The image you want your site to show when someone shares this page on social media.

* **Structured Data** - Organization: These are numerous fields to construct structured data that Google uses.  Fill this out on your home page and it will apply to all pages on your site.

Settings Tab
~~~~~~~~~~~~

The **Settings** tab is meant to house different controls for the page rendering.  You have the following options:

* **Go live date/time**: The date/time you want this page to be visible to visitors.
* **Expiry date/time**: The date/time you want this page to become invisible to visitors.
* **Content Walls**: This StreamField allows you to select Content Wall snippets that will be displayed to your users before they can access the page.  A common use case is a pop up showing them a limited offer.