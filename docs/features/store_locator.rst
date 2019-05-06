Store Locator
=============

The store locator provides pages for individual locations. These could be stores, distributors,
facilities, etc. An index page aggregates these location pages using an interactive Google Map.

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
