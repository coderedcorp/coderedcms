Events
=============

There are two abstract pages when dealing with events.  The first ``CoderedEventPage`` holds 
the information regarding the event.  Dates, location, etc all will fall under this page.  The
``CoderedEventIndexPage`` will aggregate its children ``CoderedEventPage`` and display them in a calendar.  

The event functionality is built-in to Codered CMS but it is not enabled by default.  To implement,
add the following to your ``website/models.py``::

    from modelcluster.fields import ParentalKey
    from coderedcms.models import (
        CoderedEventPage,
        CoderedEventIndexPage,
        CoderedEventOccurrence
    )

    class EventPage(CoderedEventPage):
        class Meta:
            verbose_name = 'Event Page'

        parent_page_types = ['website.EventIndexPage']
        subpage_types = []
        template = 'coderedcms/pages/event_page.html'


    class EventIndexPage(CoderedEventIndexPage):
        """
        Shows a list of event sub-pages.
        """
        class Meta:
            verbose_name = 'Events Landing Page'

        # Override to specify custom index ordering choice/default.
        NEXT_OCCURRENCE_ATTR = 'next_occurrence'
        index_query_pagemodel = 'website.EventPage'
        index_order_by_default = NEXT_OCCURRENCE_ATTR
        index_order_by_choices = (
                (NEXT_OCCURRENCE_ATTR, 'Display next occurrence, soonest first'),
            ) + \
            CoderedEventIndexPage.index_order_by_choices

        # Only allow EventPages beneath this page.
        subpage_types = ['website.EventPage']

        template = 'coderedcms/pages/event_index_page.html'


    class EventOccurrence(CoderedEventOccurrence):
        event = ParentalKey(EventPage, related_name='occurrences')


Next run ``python manage.py makemigrations`` and ``python manage.py migrate`` to create the new pages
in your project.

Now when going to the wagtail admin, you can create an EventIndexPage, and child EventPages.