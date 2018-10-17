"""
Createable pages used in CodeRed CMS.
"""
from datetime import datetime
from django.core.paginator import Paginator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from wagtail.core.utils import resolve_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel
)

from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedEmail,
    CoderedEventOccurrence,
    CoderedEventPage,
    CoderedEventTag,
    CoderedFormPage,
    CoderedPage,
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


class ArticleIndexPage(CoderedWebPage):
    """
    Shows a list of article sub-pages.
    """
    class Meta:
        verbose_name = 'Article Index Page'

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'website.ArticlePage'
    index_order_by_default = '-date_display'
    index_order_by_choices = (('-date_display', 'Display publish date, newest first'),) + \
        CoderedWebPage.index_order_by_choices
    index_show_subpages_default = True

    # Only allow ArticlePages beneath this page.
    subpage_types = ['website.ArticlePage']

    template = 'coderedcms/pages/article_index_page.html'

    show_images = models.BooleanField(
        default=True,
        verbose_name=_('Show images'),
    )
    show_captions = models.BooleanField(
        default=True,
    )
    show_meta = models.BooleanField(
        default=True,
        verbose_name=_('Show author and date info'),
    )
    show_preview_text = models.BooleanField(
        default=True,
        verbose_name=_('Show preview text'),
    )

    layout_panels = (
        CoderedWebPage.layout_panels +
        [
            MultiFieldPanel(
                [
                    FieldPanel('show_images'),
                    FieldPanel('show_captions'),
                    FieldPanel('show_meta'),
                    FieldPanel('show_preview_text'),
                ],
                heading=_('Index subpages display')
            ),
        ]
    )


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


class EventIndexPage(CoderedWebPage):
    """
    Shows a list of event sub-pages.
    """
    class Meta:
        verbose_name = 'Event Index Page'

    NEXT_OCCURRENCE_ATTR = 'next_occurrence'

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'website.EventPage'
    index_order_by_default = NEXT_OCCURRENCE_ATTR
    index_order_by_choices = (
            (NEXT_OCCURRENCE_ATTR, 'Display next occurrence, soonest first'),
        ) + \
        CoderedWebPage.index_order_by_choices
    index_show_subpages_default = True

    # Only allow EventPages beneath this page.
    subpage_types = ['website.EventPage']

    template = 'coderedcms/pages/event_index_page.html'

    show_images = models.BooleanField(
        default=True,
        verbose_name=_('Show images'),
    )
    show_meta = models.BooleanField(
        default=True,
        verbose_name=_('Show author and date info'),
    )
    show_preview_text = models.BooleanField(
        default=True,
        verbose_name=_('Show preview text'),
    )
    layout_panels = (
        CoderedWebPage.layout_panels +
        [
            MultiFieldPanel(
                [
                    FieldPanel('show_images'),
                    FieldPanel('show_meta'),
                    FieldPanel('show_preview_text'),
                ],
                heading=_('Index subpages display')
            )
        ]
    )

    def get_index_children(self):

        if self.index_query_pagemodel and self.index_order_by == self.NEXT_OCCURRENCE_ATTR:
            querymodel = resolve_model_string(self.index_query_pagemodel, self._meta.app_label)
            qs = querymodel.objects.child_of(self).live()           
            qs = sorted(qs.all(), key=lambda e: e.next_occurrence())
            return qs

        return super().get_index_children()


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
        verbose_name=_('Tags'),
        blank=True,
        help_text=_('These are ways to categorize your events.')
    )


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name='occurrences')