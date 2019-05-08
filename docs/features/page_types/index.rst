Page Types
==========

.. toctree::
    :maxdepth: 1

    article_pages
    event_pages
    form_pages
    location_pages
    web_pages


Philosophy
----------

Pages for your Codered CMS site use a "Parent-Child" relationship.  A parent page is any page that is an ancestor of other pages in the site's tree structure.  A child page is any page that is a descendant of another page in the site's tree structure.  

.. example:
    A site's page struture could look like the following:

        Home Page -> Article Landing Page -> Article Page
    
    In this example.  Home Page is a direct ancestor/parent of Article Landing Page.  Article Landing Page is a direct descendant/child of Home Page.  Article Landing Page is also a direct ancestor/parent of Article Page.  Article Page is a direct descendant/child of Article Landing Page.

===================== ====================================================================================
Parent Page Type      Child Page Types
===================== ====================================================================================
Web Page              Web Page, Article Landing Page, Event Landing Page, Location Landing Page, Form Page
Article Landing Page  Article Page
Event Landing Page    Event Page
Location Landing Page Location Page
===================== ====================================================================================
