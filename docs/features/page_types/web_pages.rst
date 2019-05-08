Web Pages
===================

The standard page for your website.  All sorts of content can exist on this page and most, if not all, other pages on the site will have similar functionality to these types of pages.

Philosophy
----------

Pages for your Codered CMS site follows the concept of "Parent-Child" relationships.  Pages that are acting as parents will typically have controls for previewing their children pages

Usage
-----

First start by creating a "Location Landing Page" (may be named differently on your specific website). Add content to this page as you would for a normal Web Page. 

Under the **Layout** tab, you have the following new options:

* Center Latitude: The latitude you want the google map to center on.
* Center Longitude: The longitude you want the google map to center on.
* Zoom: The zoom level you want hte google map to default to.  This requires an API key to use zoom. The zoom values can be between 1-20.  1: World, 5: Landmass continent, 10: City, 15: Streets, 20: Buildings

Next, save the Location Landing Page. Now create a child "Location Page" under your new "Location Landing Page". Each child page here represents a location that will have it's own page and show up in it's parent google map.  Add content to this page as you would for a normal Web Page.

Under the **Content** tab, you have the following new options:

* Address: The address of the location.
* Website: The website for the location, if applicable.
* Phone Number: The phone number of the location, if applicable.

Under the **Layout** tab, you have the following new options:

* Map Title: A custom title that will be used for this location's google map pin.  It will default to the page's normal title if not provided.
* Map Description: A custom description that will be used for this location's google map pin.

Under the **Settings** tab, you have the following new options:

* Auto Update Latitude and Longitude: If checked, the latitude and longitude will be calculated whenever the page is saved based off of the provided address.
* Latitude: The latitude that you want this location's google map pin to be set as.
* Longitude: The longitude that you want this location's google map pin to be set as.


Implementation
--------------

The store locator is built-in to CodeRed CMS but is not enabled by default. To implement, add
the following to your ``website/models.py``::

    from coderedcms.models import CoderedLocationIndexPage, CoderedLocationPage


    class LocationPage(CoderedLocationPage):
        """
        A page that holds a location.  This could be a store, a restaurant, etc.
        """
        class Meta:
            verbose_name = 'Location Page'

        template = 'coderedcms/pages/location_page.html'

        # Only allow LocationIndexPages above this page.
        parent_page_types = ['website.LocationIndexPage']


    class LocationIndexPage(CoderedLocationIndexPage):
        """
        A page that holds a list of locations and displays them with a Google Map.
        This does require a Google Maps API Key that can be defined in Settings > Google API Settings
        """
        class Meta:
            verbose_name = 'Location Landing Page'

        # Override to specify custom index ordering choice/default.
        index_query_pagemodel = 'website.LocationPage'

        # Only allow LocationPages beneath this page.
        subpage_types = ['website.LocationPage']

        template = 'coderedcms/pages/location_index_page.html'

Next run ``python manage.py makemigrations website`` and ``python manage.py migrate`` to create
the new pages in your project.

Now when going to the wagtail admin, you can create a Location Index Page, and child Location Pages.
Also be sure to add a Google Maps API key under Settings > Google API Settings.

.. note::
    Before creating or importing location pages, add your Google API key for automatic geolocation.
