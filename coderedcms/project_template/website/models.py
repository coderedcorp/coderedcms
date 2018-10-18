"""
Createable pages used in CodeRed CMS.
"""
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedEventOccurrence,
    CoderedEventPage,
    CoderedEventIndexPage,
    CoderedEventTag,
    CoderedFormPage,
    CoderedWebPage
)


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """
    class Meta:
        verbose_name = 'Article'

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['website.ArticleIndexPage']

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """
    class Meta:
        verbose_name = 'Article Landing Page'

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'website.ArticlePage'
    index_order_by_default = '-date_display'
    index_order_by_choices = (('-date_display', 'Display publish date, newest first'),) + \
        CoderedArticleIndexPage.index_order_by_choices

    # Only allow ArticlePages beneath this page.
    subpage_types = ['website.ArticlePage']

    template = 'coderedcms/pages/article_index_page.html'


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """
    class Meta:
        verbose_name = 'Form'

    template = 'coderedcms/pages/form_page.html'


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """
    page = ParentalKey('FormPage', related_name='form_fields')

class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """
    page = ParentalKey('FormPage', related_name='confirmation_emails')


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    Template renders all Navbar and Footer snippets in existance.
    """
    class Meta:
        verbose_name = 'Web Page'

    template = 'coderedcms/pages/web_page.html'


class EventTag(CoderedEventTag):
    content_object = ParentalKey('website.EventPage', related_name='event_tags')


class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = 'Event Page'

    parent_page_types = ['website.EventIndexPage']
    subpage_types = []
    template = 'coderedcms/pages/event_page.html'

    tags = ClusterTaggableManager(
        through=EventTag,
        verbose_name='Tags',
        blank=True,
        help_text='These are ways to categorize your events.'
    )


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