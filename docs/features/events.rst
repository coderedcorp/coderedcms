Events
=============

Create a calendar or list of events. Visitors can download ical invitations to their own calendars
for each event, recurring events, or all events.


Usage
-----

If events are implemented on your site (see instructions below), first start by creating an
"Event Landing Page" (may be named differently on your specific website). Add content to this
page as usual. Under the **Layout** tab, you can choose a few options:

* Show list of child pages: Check this box to show a list of all events.
* Calendar style: There are several options here. Choose one that fits your needs.

Next, save the Event Landing Page. Now create a child page. Each child page here represents
an individual event. Events can be one time, or recurring, similar to Outlook or other
calendar software.

When creating an event page, fill out the relevant information, and click the **+** icon next
to "Dates and times" to add an event occurrence. You can create multiple occurrences, or set
an occurrence to repeat.


Implementation
--------------

The event functionality is built-in to CodeRed CMS but it is not enabled by default.

There are two abstract pages when dealing with events.  The first ``CoderedEventPage`` holds
the information regarding the event.  Dates, location, etc. all will fall under this page.  The
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


Next run ``python manage.py makemigrations`` and ``python manage.py migrate`` to create the new pages
in your project.

Now when going to the wagtail admin, you can create an Event Landing Page, and child Event Pages.
