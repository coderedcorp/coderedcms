Event Pages
===========

Create a calendar or list of events. Visitors can download ical invitations to their own calendars
for each event, recurring events, or all events.


Usage
-----

First start by creating an "Event Landing Page" (may be named differently on your specific website). Add content to this page as you would for a normal Web Page. 

Under the **Layout** tab, you have the following new options:

* Show list of child pages: Check this box to show a list of all events.
* Calendar style: There are several options here. Choose one that fits your needs.

Next, save the Event Landing Page. Now create a child "Event Page" under yoru new "Event Landing Page". Each child page here represents an individual event. Events can be one time, or recurring, similar to Outlook or other calendar software. Add content to this page as you would for a normal "Web Page".

Next, save the Location Landing Page. Now create a child "Location Page" under your new "Location Landing Page". Each child page here represents a location that will have it's own page and show up in it's parent google map.  Add content to this page as you would for a normal "Web Page".

Under the **Content** tab you have the following new options:

* Calendar Color: The color that the event will have on the calendar.
* Address: The address for the event, if applicable.
* Occurrences: This lets you add the date and time information for your event.  Click the **+** icon to add a new date and time rule.

Implementation
--------------

The event functionality is built-in to CodeRed CMS but it is not enabled by default.

There are two abstract pages available when dealing with events.  The first ``CoderedEventPage`` holds
the information regarding an event.  Dates, location, etc. all will fall under this page.  The
``CoderedEventIndexPage`` will aggregate its children ``CoderedEventPage`` and display them in a
calendar or list.

To implement, add the following to your ``website/models.py``::

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

        index_query_pagemodel = 'website.EventPage'

        # Only allow EventPages beneath this page.
        subpage_types = ['website.EventPage']

        template = 'coderedcms/pages/event_index_page.html'


    class EventOccurrence(CoderedEventOccurrence):
        event = ParentalKey(EventPage, related_name='occurrences')


Next run ``python manage.py makemigrations website`` and ``python manage.py migrate`` to
create the new pages in your project.

Now when going to the wagtail admin, you can create an Event Landing Page, and child Event Pages.
