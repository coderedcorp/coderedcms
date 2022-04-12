Page Types
==========

Wagtail CRX includes several abstract page types which provided common website
functionality.

.. toctree::
    :maxdepth: 1

    article_pages
    event_pages
    form_pages
    location_pages
    stream_forms
    web_pages


Design Philosophy
-----------------

Pages in Wagtail follow a "Parent-Child" relationship.  A parent
page is any page that is an ancestor of other pages in the site's tree
structure.  A child page is any page that is a descendant of another page in the
site's tree structure.  A lot of specific site functionality is broken up into
these "Parent-Child" relationships.  For example, if you want to add a blog to
your site, you would add an "Article Landing Page", which would have your
"Article Page"s as descendants.

.. note::

    A site's page structure could look like the following:

        Home Page -> Article Landing Page -> Article Page

    In this example, Home Page is a direct ancestor/parent of Article Landing
    Page.  Article Landing Page is a direct descendant/child of Home Page.
    Article Landing Page is also a direct ancestor/parent of Article Page.
    Article Page is a direct descendant/child of Article Landing Page.

Below is a table of the current possible "Parent-Child" relationships.

===================== ====================================================================================
Parent Page Type      Child Page Types
===================== ====================================================================================
Web Page              Web Page, Article Landing Page, Event Landing Page, Location Landing Page, Form Page
Article Landing Page  Article Page
Event Landing Page    Event Page
Location Landing Page Location Page
===================== ====================================================================================

To add a new child page to any existing page, navigate to that page in the admin
and click on the "Add Child Page" button.


Development Philosophy
----------------------

When it comes to pages on the site, we strive to keep all the core functionality
in Abstract models.  When you create a new Wagtail CRX project, your generated
app will come pre-loaded with Concrete implementations of some of these Abstract
models.  These concrete models are yours to modify as needed.  But do be advised
that changing built in functionality could have untested consequences.  By
keeping the core page functionality abstract, migrations are easier to deal with
on a per project basis.
