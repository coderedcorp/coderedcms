"""
Base and abstract pages used in Wagtail CRX.
"""

import json
import logging
import os
import warnings
from datetime import date, datetime
from typing import Dict, List, Optional, TYPE_CHECKING, Union, Tuple

# This is a requirement for icalendar, even if django doesn't require it
import pytz

import geocoder
from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
)
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.core.paginator import (
    Paginator,
    InvalidPage,
    EmptyPage,
    PageNotAnInteger,
)
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from eventtools.models import BaseEvent, BaseOccurrence
from icalendar import Alarm
from icalendar import Event as ICalEvent
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from pathlib import Path
from taggit.models import TaggedItemBase
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail import hooks
from wagtail.fields import StreamField
from wagtail.models import Orderable, PageBase, Page, Site
from wagtail.coreutils import resolve_model_string
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.forms import WagtailAdminFormPageForm
from wagtail.images import get_image_model_string
from wagtail.contrib.forms.models import FormSubmission
from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod
from wagtailcache.cache import WagtailCacheMixin
from wagtailseo.models import SeoMixin, TwitterCard
from wagtailseo.utils import get_struct_data_images, StructDataEncoder

from coderedcms import utils
from coderedcms.blocks import (
    CONTENT_STREAMBLOCKS,
    LAYOUT_STREAMBLOCKS,
    STREAMFORM_BLOCKS,
    ContentWallBlock,
)
from coderedcms.fields import CoderedStreamField, ColorField
from coderedcms.forms import CoderedFormBuilder, CoderedSubmissionsListView
from coderedcms.models.snippet_models import ClassifierTerm
from coderedcms.models.wagtailsettings_models import LayoutSettings
from coderedcms.wagtail_flexible_forms.blocks import (
    FormFieldBlock,
    FormStepBlock,
)
from coderedcms.wagtail_flexible_forms.models import (
    Step,
    Steps,
    StreamFormMixin,
    StreamFormJSONEncoder,
    SessionFormSubmission,
    SubmissionRevision,
)
from coderedcms.settings import crx_settings
from coderedcms.widgets import ClassifierSelectWidget


if TYPE_CHECKING:
    from wagtail.images.models import AbstractImage


logger = logging.getLogger("coderedcms")


CRX_PAGE_MODELS = []


def get_page_models():
    return CRX_PAGE_MODELS


class CoderedPageMeta(PageBase):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if not cls._meta.abstract:
            CRX_PAGE_MODELS.append(cls)


class CoderedTag(TaggedItemBase):
    class Meta:
        verbose_name = _("CodeRed Tag")

    content_object = ParentalKey(
        "coderedcms.CoderedPage", related_name="tagged_items"
    )


class CoderedPage(WagtailCacheMixin, SeoMixin, Page, metaclass=CoderedPageMeta):
    """
    General use page with caching, templating, and SEO functionality.
    All pages should inherit from this.
    """

    class Meta:
        verbose_name = _("CodeRed Page")

    # Do not allow this page type to be created in wagtail admin
    is_creatable = False

    # Templates
    # The page will render the following templates under certain conditions:
    #
    # template = ''
    # ajax_template = ''
    # search_template = ''

    # Template used in site search results.
    search_template = "coderedcms/pages/search_result.html"

    # Template used for related pages, Latest Pages block, and Page Preview block.
    miniview_template = "coderedcms/pages/page.mini.html"

    ###############
    # Content fields
    ###############

    cover_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Cover image"),
    )

    ###############
    # Index fields
    ###############

    # Subclasses can override this to enabled index features by default.
    index_show_subpages_default = False

    # Subclasses can override this to query on a specific
    # page model, rather than the default wagtail Page.
    index_query_pagemodel = "coderedcms.CoderedPage"

    # Subclasses can override these fields to enable custom
    # ordering based on specific subpage fields.
    index_order_by_default = ""
    index_order_by_choices = (
        ("", _("Default Ordering")),
        ("-first_published_at", _("Date first published, newest to oldest")),
        ("first_published_at", _("Date first published, oldest to newest")),
        ("-last_published_at", _("Date updated, newest to oldest")),
        ("last_published_at", _("Date updated, oldest to newest")),
        ("title", _("Title, alphabetical")),
        ("-title", _("Title, reverse alphabetical")),
    )
    index_show_subpages = models.BooleanField(
        default=index_show_subpages_default,
        verbose_name=_("Show list of child pages"),
    )
    index_order_by_classifier = models.ForeignKey(
        "coderedcms.Classifier",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Order child pages by classifier"),
        help_text=_(
            "Child pages will first be sorted following the order of this "
            "classifier’s terms (from Snippets > Classifiers)."
        ),
    )
    index_order_by = models.CharField(
        max_length=255,
        choices=index_order_by_choices,
        default=index_order_by_default,
        blank=True,
        verbose_name=_("Order child pages by"),
        help_text=_("Child pages will then be sorted by this attribute."),
    )
    index_num_per_page = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Number per page"),
    )
    index_classifiers = ParentalManyToManyField(
        "coderedcms.Classifier",
        blank=True,
        verbose_name=_("Filter child pages by"),
        help_text=_("Enable filtering child pages by these classifiers."),
    )

    #####################
    # Related Page Fields
    #####################

    # Subclasses can override this to query on a specific page model, in the
    # format "appname.Model". By default sibling pages are used.
    related_query_pagemodel = None

    # Subclasses can override this to enabled related pages by default.
    related_show_default = False

    related_show = models.BooleanField(
        default=related_show_default,
        verbose_name=_("Show list of related pages"),
    )

    related_num = models.PositiveIntegerField(
        default=3,
        verbose_name=_("Number of related pages to show"),
    )

    related_classifier_term = models.ForeignKey(
        "coderedcms.ClassifierTerm",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Preferred related classifier term"),
        help_text=_(
            "When getting related pages, pages with this term will be "
            "weighted over other classifier terms. By default, pages with "
            "the greatest number of classifiers in common are ranked highest."
        ),
    )

    ###############
    # Layout fields
    ###############

    custom_template = models.CharField(
        blank=True, max_length=255, choices=None, verbose_name=_("Template")
    )

    ###############
    # SEO overrides
    ###############

    seo_image_sources = [
        "og_image",
        "cover_image",
    ]

    ###############
    # Classify
    ###############

    classifier_terms = ParentalManyToManyField(
        "coderedcms.ClassifierTerm",
        blank=True,
        verbose_name=_("Classifiers"),
        help_text=_(
            "Categorize and group pages together with classifiers. "
            "Used to organize and filter pages across the site."
        ),
    )
    tags = ClusterTaggableManager(
        through=CoderedTag,
        blank=True,
        verbose_name=_("Tags"),
        help_text=_("Used to organize pages across the site."),
    )

    ###############
    # Settings
    ###############

    content_walls = CoderedStreamField(
        [("content_wall", ContentWallBlock())],
        blank=True,
        use_json_field=True,
        verbose_name=_("Content Walls"),
    )

    ###############
    # Search
    ###############

    search_fields = Page.search_fields + [
        index.SearchField("seo_title", boost=2),
        index.SearchField("search_description", boost=2),
        index.FilterField("index_show_subpages"),
        index.FilterField("index_order_by"),
        index.FilterField("custom_template"),
        index.FilterField("classifier_terms"),
    ]

    ###############
    # Panels
    ###############

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
    ]

    body_content_panels = []

    bottom_content_panels = []

    classify_panels = [
        FieldPanel("classifier_terms", widget=ClassifierSelectWidget()),
        FieldPanel("tags"),
    ]

    layout_panels = [
        MultiFieldPanel(
            [FieldPanel("custom_template")], heading=_("Visual Design")
        ),
        MultiFieldPanel(
            [
                FieldPanel("index_show_subpages"),
                FieldPanel("index_num_per_page"),
                FieldPanel("index_order_by_classifier"),
                FieldPanel("index_order_by"),
                FieldPanel(
                    "index_classifiers", widget=forms.CheckboxSelectMultiple()
                ),
            ],
            heading=_("Show Child Pages"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("related_show"),
                FieldPanel("related_num"),
                FieldPanel("related_classifier_term"),
            ],
            heading=_("Related Pages"),
        ),
    ]

    promote_panels = SeoMixin.seo_meta_panels + SeoMixin.seo_struct_panels

    settings_panels = Page.settings_panels + [
        FieldPanel("content_walls"),
    ]

    integration_panels = []

    def __init__(self, *args, **kwargs):
        """
        Inject custom choices and defaults into the form fields
        to enable customization by subclasses.
        """
        super().__init__(*args, **kwargs)
        klassname = self.__class__.__name__.lower()
        template_choices = crx_settings.CRX_FRONTEND_TEMPLATES_PAGES.get(
            "*", []
        ) + crx_settings.CRX_FRONTEND_TEMPLATES_PAGES.get(klassname, [])

        self._meta.get_field("index_order_by").choices = (
            self.index_order_by_choices
        )
        self._meta.get_field("custom_template").choices = template_choices
        if not self.id:
            self.index_order_by = self.index_order_by_default
            self.index_show_subpages = self.index_show_subpages_default
            self.related_show = self.related_show_default

    @cached_classmethod
    def get_edit_handler(cls):
        """
        Override to "lazy load" the panels overridden by subclasses.
        """
        panels = [
            ObjectList(
                cls.content_panels
                + cls.body_content_panels
                + cls.bottom_content_panels,
                heading=_("Content"),
            ),
            ObjectList(cls.classify_panels, heading=_("Classify")),
            ObjectList(cls.layout_panels, heading=_("Layout")),
            ObjectList(cls.promote_panels, heading=_("SEO"), classname="seo"),
            ObjectList(
                cls.settings_panels, heading=_("Settings"), classname="settings"
            ),
        ]

        if cls.integration_panels:
            panels.append(
                ObjectList(
                    cls.integration_panels,
                    heading="Integrations",
                    classname="integrations",
                )
            )

        edit_handler = TabbedInterface(panels)
        return edit_handler.bind_to_model(cls)

    @property
    def seo_logo(self) -> "Optional[AbstractImage]":
        """
        Override method in SeoMixin.
        Gets the primary logo of the organization.
        """
        logo = super().seo_logo
        if logo:
            return logo
        else:
            layout_settings = LayoutSettings.for_site(self.get_site())
            if layout_settings.logo:
                return layout_settings.logo
        return None

    @property
    def seo_image(self) -> "Optional[AbstractImage]":
        """
        Override method in SeoMixin.
        Fallback to logo if opengraph image is not specified.
        """
        img = super().seo_image
        if img is None:
            return self.seo_logo
        return img

    @property
    def seo_twitter_card_content(self) -> str:
        """
        Override of method in SeoMixin.
        Show a large twitter card if the page has an image set.
        """
        if self.seo_image:
            return TwitterCard.LARGE.value
        return self.seo_twitter_card.value

    def get_template(self, request, *args, **kwargs):
        """
        Override parent to serve different templates based on querystring.
        """
        if self.custom_template:
            return self.custom_template

        return super().get_template(request, args, kwargs)

    def get_index_children(self):
        """
        Returns query of subpages as defined by `index_` variables.
        """
        if self.index_query_pagemodel:
            querymodel = resolve_model_string(
                self.index_query_pagemodel, self._meta.app_label
            )
            query = querymodel.objects.child_of(self).live()
        else:
            query = self.get_children().live()

        # Determine query sorting order.
        order = []

        # To sort by term order of a specific classifier, annotate the child
        # pages with the `sort_order` of its ClassifierTerms.
        if self.index_order_by_classifier:
            terms = ClassifierTerm.objects.filter(
                classifier=self.index_order_by_classifier,
                # Reverse ManyToMany of `coderedpage.classifier_terms`.
                coderedpage=models.OuterRef("pk"),
            )[:1]
            query = query.annotate(
                term_sort_order=models.Subquery(terms.values("sort_order"))
            )
            order.append("term_sort_order")

        # Second, order by the specified model attribute.
        if self.index_order_by:
            order.append(self.index_order_by)

        # Order the query.
        if order:
            query = query.order_by(*order)

        return query

    def get_related_pages(
        self, pagetype: str = None, num: int = None
    ) -> models.QuerySet:
        """
        Returns a queryset of sibling pages, or the model type
        defined by ``pagetype`` or ``self.related_query_pagemodel``,
        ordered by number of shared classifier terms.

        :param str pagetype: The model type to query on. This should
          be a string in the format "appname.Model".
          Overrides ``self.related_query_pagemodel``

        :param int num: The number of results to return.
          Overrides ``self.related_num``.
        """

        if pagetype is None:
            pagetype = self.related_query_pagemodel

        if num is None:
            num = self.related_num

        # Get our related query model, and queryset.
        if pagetype:
            querymodel = resolve_model_string(pagetype, self._meta.app_label)
            r_qs = querymodel.objects.all().live()
        else:
            r_qs = self.get_parent().specific.get_index_children()

        # Exclude self to avoid infinite recursion.
        r_qs = r_qs.exclude(pk=self.pk)

        order_by = []

        # If we have a preferred classifier term, order by that.
        if self.related_classifier_term:
            p_ct_q = models.Q(classifier_terms=self.related_classifier_term)
            r_qs = r_qs.annotate(p_ct=p_ct_q)
            order_by.append("-p_ct")

        # If this page has a classifier, then order by number of
        # shared classifier terms.
        if self.classifier_terms.exists():
            r_ct_q = models.Q(classifier_terms__in=self.classifier_terms.all())
            r_qs = r_qs.annotate(r_ct=models.Count("classifier_terms", r_ct_q))
            order_by.append("-r_ct")

        # Order the related pages, then add distinct to deal with
        # annotating based on a many to many.
        if order_by:
            r_qs = r_qs.order_by(*order_by).distinct()

        return r_qs[:num]

    def get_content_walls(self, check_child_setting=True):
        current_content_walls = []
        if check_child_setting:
            for wall in self.content_walls:
                if wall.value["show_content_wall_on_children"]:
                    current_content_walls.append(wall.value)
        else:
            current_content_walls = self.content_walls

        try:
            return (
                list(current_content_walls)
                + self.get_parent().specific.get_content_walls()
            )
        except AttributeError:
            return list(current_content_walls)

    def get_context(self, request, *args, **kwargs):
        """
        Add child pages and paginated child pages to context.
        """
        context = super().get_context(request)

        # Show list of child pages.
        if self.index_show_subpages:
            # Get child pages
            all_children = self.get_index_children()
            # Filter by classifier terms if applicable
            if len(request.GET) > 0 and self.index_classifiers.exists():
                # Look up comma separated ClassifierTerm slugs
                # i.e. `/?c=term1-slug,term2-slug`
                terms = []
                get_c = request.GET.get("c", None)
                if get_c:
                    terms = get_c.split(",")
                # Else look up individual querystrings
                # i.e. `/?classifier-slug=term1-slug`
                else:
                    for classifier in self.index_classifiers.all().only("slug"):
                        get_term = request.GET.get(classifier.slug, None)
                        if get_term:
                            terms.append(get_term)
                if len(terms) > 0:
                    selected_terms = ClassifierTerm.objects.filter(
                        slug__in=terms
                    )
                    context["selected_terms"] = selected_terms
                    if len(selected_terms) > 0:
                        try:
                            for term in selected_terms:
                                all_children = all_children.filter(
                                    classifier_terms=term
                                )
                        except AttributeError:
                            logger.warning(
                                (
                                    "Tried to filter by ClassifierTerm, "
                                    "but <%s.%s ('%s')>.get_index_children() "
                                    "did not return a queryset or is not a "
                                    "queryset of CoderedPage models."
                                ),
                                self._meta.app_label,
                                self.__class__.__name__,
                                self.title,
                            )
            paginator = Paginator(all_children, self.index_num_per_page)
            pagenum = request.GET.get("p", 1)
            try:
                paged_children = paginator.page(pagenum)
            except (PageNotAnInteger, EmptyPage, InvalidPage):
                paged_children = paginator.page(1)

            context["index_paginated"] = paged_children
            context["index_children"] = all_children

        # Show a list of related pages.
        if self.related_show:
            context["related_pages"] = self.get_related_pages()

        # Content walls.
        context["content_walls"] = self.get_content_walls(
            check_child_setting=False
        )

        return context


###############################################################################
# Abstract pages providing pre-built common website functionality, suitable for subclassing.
# These are abstract so subclasses can override fields if desired.
###############################################################################


class CoderedWebPage(CoderedPage):
    """
    Provides a body and body-related functionality.
    This is abstract so that subclasses can override the body StreamField.
    """

    class Meta:
        verbose_name = _("CodeRed Web Page")
        abstract = True

    template = "coderedcms/pages/web_page.html"

    # Child pages should override based on what blocks they want in the body.
    # Default is LAYOUT_STREAMBLOCKS which is the fullest editor experience.
    body = StreamField(
        LAYOUT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    # Search fields
    search_fields = CoderedPage.search_fields + [index.SearchField("body")]

    # Panels
    body_content_panels = [
        FieldPanel("body"),
    ]

    @property
    def body_preview(self):
        """
        A shortened version of the body without HTML tags.
        """
        # add spaces between tags for legibility
        body = str(self.body).replace(">", "> ")
        # strip tags
        body = strip_tags(body)
        # truncate and add ellipses
        preview = body[:200] + "..." if len(body) > 200 else body
        return mark_safe(preview)


class CoderedArticlePage(CoderedWebPage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = _("CodeRed Article")
        abstract = True

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"

    related_show_default = True

    # Override body to provide simpler content
    body = StreamField(
        CONTENT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Caption"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Author"),
    )
    author_display = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Display author as"),
        help_text=_("Override how the author’s name displays on this article."),
    )
    date_display = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Display publish date"),
    )

    def get_author_name(self):
        warnings.warn(
            (
                "CoderedArticlePage.get_author_name has been replaced with "
                "CoderedArticlePage.seo_author"
            ),
            DeprecationWarning,
        )
        return self.seo_author

    @property
    def seo_author(self) -> str:
        """
        Override of method in SeoMixin.
        Gets author name using a fallback.
        """
        if self.author_display:
            return self.author_display
        if self.author:
            return self.author.get_full_name()
        if self.owner:
            return self.owner.get_full_name()
        return ""

    def get_pub_date(self):
        warnings.warn(
            (
                "CoderedArticlePage.get_pub_date has been replaced with "
                "CoderedArticlePage.seo_published_at"
            ),
            DeprecationWarning,
        )
        return self.seo_published_at

    @property
    def seo_published_at(self) -> datetime:
        """
        Override of method in SeoMixin.
        Gets published date.
        """
        if self.date_display:
            return self.date_display
        return self.first_published_at

    def get_description(self):
        warnings.warn(
            (
                "CoderedArticlePage.get_description has been replaced with "
                "CoderedArticlePage.seo_description"
            ),
            DeprecationWarning,
        )
        return self.seo_description

    @property
    def seo_description(self) -> str:
        """
        Override of method in SeoMixin.
        Gets the description using a fallback.
        """
        if self.search_description:
            return self.search_description
        if self.caption:
            return self.caption
        if self.body_preview:
            return self.body_preview
        return ""

    search_fields = CoderedWebPage.search_fields + [
        index.SearchField("caption", boost=2),
        index.FilterField("author"),
        index.FilterField("author_display"),
        index.FilterField("date_display"),
    ]

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("caption"),
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("author_display"),
                FieldPanel("date_display"),
            ],
            _("Publication Info"),
        ),
    ]


class CoderedArticleIndexPage(CoderedWebPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = _("CodeRed Article Index Page")
        abstract = True

    template = "coderedcms/pages/article_index_page.html"

    index_show_subpages_default = True

    index_order_by_default = "-date_display"
    index_order_by_choices = (
        ("-date_display", "Display publish date, newest first"),
    ) + CoderedWebPage.index_order_by_choices

    show_images = models.BooleanField(
        default=True,
        verbose_name=_("Show images"),
    )
    show_captions = models.BooleanField(
        default=True,
    )
    show_meta = models.BooleanField(
        default=True,
        verbose_name=_("Show author and date info"),
    )
    show_preview_text = models.BooleanField(
        default=True,
        verbose_name=_("Show preview text"),
    )

    layout_panels = CoderedWebPage.layout_panels + [
        MultiFieldPanel(
            [
                FieldPanel("show_images"),
                FieldPanel("show_captions"),
                FieldPanel("show_meta"),
                FieldPanel("show_preview_text"),
            ],
            heading=_("Child page display"),
        ),
    ]


class CoderedEventPage(CoderedWebPage, BaseEvent):
    class Meta:
        verbose_name = _("CodeRed Event")
        abstract = True

    calendar_color = ColorField(
        blank=True,
        help_text=_(
            "The color that the event will use when displayed on a calendar."
        ),
    )
    address = models.TextField(blank=True, verbose_name=_("Address"))
    content_panels = CoderedWebPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("calendar_color"),
                FieldPanel("address"),
            ],
            heading=_("Event information"),
        ),
        InlinePanel(
            "occurrences",
            min_num=1,
            heading=_("Dates and times"),
        ),
    ]

    @property
    def upcoming_occurrences(self):
        """
        Returns the next x occurrences for this event.
        By default, it returns 10.
        """
        return self.query_occurrences(num_of_instances_to_return=10)

    @property
    def most_recent_occurrence(
        self,
    ) -> Tuple[datetime, datetime, BaseOccurrence]:
        """
        Gets the next upcoming, or last occurrence if the event has no more occurrences.
        """

        try:
            noc = self.next_occurrence()
            if noc:
                return noc

        except AttributeError:
            # Triggers when a preview is initiated on an
            # EventPage because it uses a FakeQuerySet object.
            # Here we manually compute the next_occurrence
            occurrences = [e.next_occurrence() for e in self.occurrences.all()]
            # If there are no more occurrences, we find the last one instead
            if occurrences and None not in occurrences:
                return sorted(occurrences, key=lambda tup: tup[0])[0]

        # If both of the above methods fail to find a future occurrence,
        # instead return the last occurrence.
        aoc = []
        for occurrence in self.occurrences.all():
            aoc += [instance for instance in occurrence.all_occurrences()]
        if len(aoc) > 0:
            return aoc[-1]  # last one in the list

    @property
    def seo_struct_event_dict(self) -> dict:
        next_occ = self.most_recent_occurrence
        if not next_occ:
            return {}
        # The method returns a tuple of the start, end, and object. We only care about
        # the object, so take it out of the tuple.
        next_occ = next_occ[2]
        sd_dict = {
            "@context": "https://schema.org/",
            "@type": "Event",
            "name": self.title,
            "description": self.seo_description,
            "startDate": next_occ.start,
            "endDate": next_occ.end,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": self.get_full_url(),
            },
        }

        if self.seo_image:
            sd_dict.update(
                {
                    "image": get_struct_data_images(
                        self.get_site(), self.seo_image
                    )
                }
            )

        if self.address:
            sd_dict.update(
                {
                    "location": {
                        "@type": "Place",
                        "name": self.title,
                        "address": {
                            "@type": "PostalAddress",
                            "streetAddress": self.address,
                        },
                    },
                }
            )

        return sd_dict

    @property
    def seo_struct_event_json(self) -> str:
        return json.dumps(self.seo_struct_event_dict, cls=StructDataEncoder)

    def query_occurrences(self, num_of_instances_to_return=None, **kwargs):
        """
        Returns a list of all upcoming event instances for the specified query.
        For more information on what you can query with, visit
        https://github.com/gregplaysguitar/django-eventtools
        """
        event_instances = []
        occurrence_kwargs = {
            "from_date": kwargs.get("from_date", timezone.now().date())
        }

        if "limit" in kwargs:
            if kwargs["limit"] is not None:
                # Limit the number of event instances that will be
                # generated per occurrence rule to 10, if not otherwise specified.
                occurrence_kwargs["limit"] = kwargs.get("limit", 10)

        # For each occurrence rule in all of the occurrence rules for this event.
        for occurrence in self.occurrences.all():
            # Add the qualifying generated event instances to the list.
            event_instances += [
                instance
                for instance in occurrence.all_occurrences(**occurrence_kwargs)
            ]

        # Sort all the events by the date that they start
        event_instances.sort(key=lambda d: d[0])

        # Return the event instances, possibly spliced if num_instances_to_return is set.
        return (
            event_instances[:num_of_instances_to_return]
            if num_of_instances_to_return
            else event_instances
        )

    def convert_to_ical_format(
        self,
        dt_start: datetime = None,
        dt_end: datetime = None,
        occurrence=None,
    ):
        ical_event = ICalEvent()
        ical_event.add("summary", self.title)
        # needs to get full page url, not just slug
        desc_str = _("Details")
        ical_event.add("dtstamp", timezone.now())
        ical_event.add("description", f"{desc_str}: {self.full_url}")
        # NOTE: The use of the url for the id is technically breaking the iCal standard,
        #  which recommends against use of identifiable info:
        # https://icalendar.org/New-Properties-for-iCalendar-RFC-7986/5-3-uid-property.html
        # If this breaks in the future,
        # implementing a uuid field on the object is probably necessary.
        ical_event.add("uid", self.get_full_url())
        if self.address:
            ical_event.add("location", self.address)

        if dt_start:
            # Convert to utc to remove timezone confusion
            dt_start = dt_start.astimezone(pytz.utc)
            ical_event.add("dtstart", dt_start)

            if dt_end:
                # Convert to utc to remove timezone confusion
                dt_end = dt_end.astimezone(pytz.utc)
                ical_event.add("dtend", dt_end)

            # Add a reminder alarm
            reminder_mins = 15
            alarm = Alarm()
            alarm.add("action", "DISPLAY")
            alarm.add("description", "Reminder")
            # Sets the reminder alarm
            alarm.add("TRIGGER;RELATED=START", "-PT{0}M".format(reminder_mins))
            ical_event.add_component(alarm)

        if occurrence:
            freq = (
                occurrence.repeat.split(":")[1] if occurrence.repeat else None
            )
            repeat_until = (
                occurrence.repeat_until.strftime("%Y%m%dT000000Z")
                if occurrence.repeat_until
                else None
            )

            ical_event.add("dtstart", occurrence.start)

            if occurrence.end:
                ical_event.add("dtend", occurrence.end)

            if freq:
                ical_event.add("RRULE", freq, encode=False)

            if repeat_until:
                ical_event.add("until", repeat_until)

        return ical_event

    def create_single_ical(self, dt_start, dt_end=None):
        return self.convert_to_ical_format(dt_start=dt_start, dt_end=dt_end)

    def create_recurring_ical(self):
        events = []
        for occurrence in self.occurrences.all():
            events.append(self.convert_to_ical_format(occurrence=occurrence))
        return events


class CoderedEventIndexPage(CoderedWebPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = _("CodeRed Event Index Page")
        abstract = True

    class CalendarViews(models.TextChoices):
        NONE = "", _("No calendar")
        MONTH = "month", _("Month")
        AGENDA_WEEK = "agendaWeek", _("Week")
        AGENDA_DAY = "agendaDay", _("Day")
        LIST_MONTH = "listMonth", _("List of events")

    class EventStyles(models.TextChoices):
        DEFAULT = "", _("Default")
        BLOCK = "block", _("Solid rectangles")
        DOT = "list-item", _("Dots with labels")

    template = "coderedcms/pages/event_index_page.html"

    index_show_subpages_default = True

    index_order_by_default = "next_occurrence"
    index_order_by_choices = (
        ("next_occurrence", "Display next occurrence, soonest first"),
    ) + CoderedWebPage.index_order_by_choices

    default_calendar_view = models.CharField(
        blank=True,
        choices=CalendarViews.choices,
        default=CalendarViews.MONTH,
        max_length=255,
        verbose_name=_("Calendar Style"),
        help_text=_("The default look of the calendar on this page."),
    )
    event_style = models.CharField(
        blank=True,
        choices=EventStyles.choices,
        default=EventStyles.DEFAULT,
        max_length=255,
        verbose_name=_("Event Style"),
        help_text=_("How events look on the calendar."),
    )

    layout_panels = CoderedWebPage.layout_panels + [
        MultiFieldPanel(
            [
                FieldPanel("default_calendar_view"),
                FieldPanel("event_style"),
            ],
            heading=_("Calendar Style"),
        )
    ]

    @property
    def fullcalendar_view(self) -> str:
        """
        Translate calendar views to fullcalendar.js identifiers.
        """
        return {
            self.CalendarViews.NONE: "",
            self.CalendarViews.MONTH: "dayGridMonth",
            self.CalendarViews.AGENDA_WEEK: "timeGridWeek",
            self.CalendarViews.AGENDA_DAY: "timeGridDay",
            self.CalendarViews.LIST_MONTH: "listMonth",
        }[self.default_calendar_view]

    @property
    def fullcalendar_event_display(self) -> str:
        """
        Translate event display styles to fullcalendar.js identifiers.
        """
        return {
            self.EventStyles.DEFAULT: "auto",
            self.EventStyles.BLOCK: "block",
            self.EventStyles.DOT: "list-item",
        }[self.event_style]

    def get_index_children(self):
        if (
            self.index_query_pagemodel
            and self.index_order_by == "next_occurrence"
        ):
            querymodel = resolve_model_string(
                self.index_query_pagemodel, self._meta.app_label
            )
            qs = querymodel.objects.child_of(self).live()
            # filter out events that don't have a next_occurrence
            upcoming = []
            for event in qs.all():
                if event.next_occurrence():
                    upcoming.append(event)
            # Sort the events by next_occurrence start date.
            return sorted(upcoming, key=lambda e: e.next_occurrence()[0])

        return super().get_index_children()

    def get_calendar_events(
        self, start: Union[datetime, date], end: Union[datetime, date]
    ) -> List[Dict[str, str]]:
        """
        Returns a list of event occurrences as dictionaries with times
        converted to Django TIME_ZONE settings.
        """
        # start with all child events, regardless of get_index_children rules.
        querymodel = resolve_model_string(
            self.index_query_pagemodel, self._meta.app_label
        )
        qs = querymodel.objects.child_of(self).live()
        event_instances = []
        for event in qs:
            occurrences = event.query_occurrences(
                limit=None, from_date=start, to_date=end
            )
            for occurrence in occurrences:
                local_start = timezone.localtime(value=occurrence[0])
                local_end = None
                if occurrence[1]:
                    local_end = timezone.localtime(value=occurrence[1])
                event_data = {
                    "title": event.title,
                    "start": local_start.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "end": (
                        local_end.strftime("%Y-%m-%dT%H:%M:%S%z")
                        if local_end
                        else ""
                    ),
                    "description": "",
                }
                if event.url:
                    event_data["url"] = event.url
                if event.calendar_color:
                    event_data["color"] = event.calendar_color
                event_instances.append(event_data)
        return event_instances


class CoderedEventOccurrence(Orderable, BaseOccurrence):
    class Meta(Orderable.Meta):
        verbose_name = _("CodeRed Event Occurrence")
        abstract = True


class CoderedFormMixin(models.Model):
    class Meta:
        abstract = True

    submissions_list_view_class = CoderedSubmissionsListView
    encoder = DjangoJSONEncoder

    # Custom codered fields
    to_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Email form submissions to"),
        help_text=_(
            "Optional - email form submissions to this address. "
            "Separate multiple addresses by comma."
        ),
    )
    reply_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Reply-to address"),
        help_text=_(
            "Optional - to reply to the submitter, specify the email field here. "
            "For example, if a form field above is labeled "
            '"Your Email", enter: {{ your_email }}'
        ),
    )
    subject = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Subject"),
    )
    save_to_database = models.BooleanField(
        default=True,
        verbose_name=_("Save form submissions"),
        help_text=_(
            "Submissions are saved to database and can be exported at any time."
        ),
    )
    thank_you_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Thank you page"),
        help_text=_(
            "The page users are redirected to after submitting the form."
        ),
    )
    button_text = models.CharField(
        max_length=255,
        default=_("Submit"),
        verbose_name=_("Button text"),
    )
    button_style = models.CharField(
        blank=True,
        choices=crx_settings.CRX_FRONTEND_BTN_STYLE_CHOICES,
        default=crx_settings.CRX_FRONTEND_BTN_STYLE_DEFAULT,
        max_length=255,
        verbose_name=_("Button style"),
    )
    button_size = models.CharField(
        blank=True,
        choices=crx_settings.CRX_FRONTEND_BTN_SIZE_CHOICES,
        default=crx_settings.CRX_FRONTEND_BTN_SIZE_DEFAULT,
        max_length=255,
        verbose_name=_("Button Size"),
    )
    button_css_class = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Button CSS class"),
        help_text=_("Custom CSS class applied to the submit button."),
    )
    form_css_class = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Form CSS Class"),
        help_text=_("Custom CSS class applied to <form> element."),
    )
    form_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Form ID"),
        help_text=_("Custom ID applied to <form> element."),
    )
    form_golive_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Form go live date/time"),
        help_text=_("Date and time when the FORM goes live on the page."),
    )
    form_expire_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Form expiry date/time"),
        help_text=_(
            "Date and time when the FORM will no longer be available on the page."
        ),
    )
    spam_protection = models.BooleanField(
        default=True,
        verbose_name=_("Spam Protection"),
        help_text=_(
            "When enabled, the CMS will filter out spam form submissions for this page."
        ),
    )

    body_content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("thank_you_page"),
                FieldPanel("button_text"),
                FieldPanel("button_style"),
                FieldPanel("button_size"),
                FieldPanel("button_css_class"),
                FieldPanel("form_css_class"),
                FieldPanel("form_id"),
            ],
            _("Form Settings"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("save_to_database"),
                FieldPanel("to_address"),
                FieldPanel("reply_address"),
                FieldPanel("subject"),
            ],
            _("Form Submissions"),
        ),
    ]

    settings_panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("form_golive_at"),
                        FieldPanel("form_expire_at"),
                    ],
                    classname="label-above",
                ),
            ],
            _("Form Scheduled Publishing"),
        ),
        FieldPanel("spam_protection"),
    ]

    @property
    def form_live(self):
        """
        A boolean on whether or not the <form> element should be shown on the page.
        """
        return (
            self.form_golive_at is None or self.form_golive_at <= timezone.now()
        ) and (
            self.form_expire_at is None or self.form_expire_at >= timezone.now()
        )

    def get_landing_page_template(self, request, *args, **kwargs):
        return self.landing_page_template

    def process_data(self, form, request):
        processed_data = {}
        # Handle file uploads
        for key, val in form.cleaned_data.items():
            if (
                type(val) is InMemoryUploadedFile
                or type(val) is TemporaryUploadedFile
            ):
                # Save the file and get its URL

                # Custom code to ensure that anonymous users get a session key.
                if not request.session.session_key:
                    request.session.create()

                directory = request.session.session_key
                storage = self.get_storage()
                Path(storage.path(directory)).mkdir(parents=True, exist_ok=True)
                path = storage.get_available_name(
                    str(Path(directory) / val.name)
                )
                with storage.open(path, "wb+") as destination:
                    for chunk in val.chunks():
                        destination.write(chunk)

                processed_data[key] = "{0}{1}".format(
                    crx_settings.CRX_PROTECTED_MEDIA_URL, path
                )
            else:
                processed_data[key] = val

        return processed_data

    def get_storage(self):
        return FileSystemStorage(
            location=crx_settings.CRX_PROTECTED_MEDIA_ROOT,
            base_url=crx_settings.CRX_PROTECTED_MEDIA_URL,
        )

    def process_form_submission(
        self, request, form, form_submission, processed_data
    ):
        # Save to database
        if self.save_to_database:
            form_submission.save()

        # Send the mails
        if self.to_address:
            self.send_summary_mail(request, form, processed_data)

        if self.confirmation_emails:
            # Convert form data into a context.
            context = Context(self.data_to_dict(processed_data, request))
            # Render emails as if they are django templates.
            for email in self.confirmation_emails.all():
                # Build email message parameters.
                message_args = {}
                # From
                if email.from_address:
                    template_from_email = Template(email.from_address)
                    message_args["from_email"] = template_from_email.render(
                        context
                    )
                else:
                    genemail = LayoutSettings.for_request(
                        request
                    ).from_email_address
                    if genemail:
                        message_args["from_email"] = genemail
                # Reply-to
                if email.reply_address:
                    template_reply_to = Template(email.reply_address)
                    message_args["reply_to"] = template_reply_to.render(
                        context
                    ).split(",")
                # CC
                if email.cc_address:
                    template_cc = Template(email.cc_address)
                    message_args["cc"] = template_cc.render(context).split(",")
                # BCC
                if email.bcc_address:
                    template_bcc = Template(email.bcc_address)
                    message_args["bcc"] = template_bcc.render(context).split(
                        ","
                    )
                # Subject
                if email.subject:
                    template_subject = Template(email.subject)
                    message_args["subject"] = template_subject.render(context)
                else:
                    message_args["subject"] = self.title
                # Body
                template_body = Template(email.body)
                message_args["body"] = template_body.render(context)
                # To
                template_to = Template(email.to_address)
                message_args["to"] = template_to.render(context).split(",")

                # Send email
                self.send_mail(request, message_args, "html")

        for fn in hooks.get_hooks("form_page_submit"):
            fn(instance=self, form_submission=form_submission)

    def send_summary_mail(self, request, form, processed_data):
        """
        Sends a form submission summary email.
        """
        addresses = [x.strip() for x in self.to_address.split(",")]
        content = []
        data = self.data_to_dict(processed_data, request)

        for field in form:
            # Get key from form, transform same as data_to_dict() does.
            key = field.html_name.replace("-", "_")
            label = field.label
            value = data.get(key)
            content.append("{0}: {1}".format(label, value))

        content_str = "\n-------------------- \n".join(content) + "\n"

        # Build email message parameters
        message_args = {
            "body": content_str,
            "to": addresses,
        }
        if self.subject:
            message_args["subject"] = self.subject
        else:
            message_args["subject"] = self.title
        genemail = LayoutSettings.for_request(request).from_email_address
        if genemail:
            message_args["from_email"] = genemail
        if self.reply_address:
            # Render reply-to field using form submission as context.
            context = Context(data)
            template_reply_to = Template(self.reply_address)
            message_args["reply_to"] = template_reply_to.render(context).split(
                ","
            )

        # Send email
        self.send_mail(request, message_args)

    def send_mail(
        self, resuest, message_args: dict, content_subtype: Optional[str] = None
    ):
        """
        Utility to send email messages from form submissions.

        You can override this method to have the form send mail in a different
        way or using a different backend as needed.
        """
        message = EmailMessage(**message_args)
        if content_subtype:
            message.content_subtype = content_subtype
        message.send()

    def render_landing_page(self, request, form_submission=None):
        """
        Renders the landing page.

        You can override this method to return a different HttpResponse as
        landing page. E.g. you could return a redirect to a separate page.
        """
        if self.thank_you_page:
            return redirect(self.thank_you_page.url)

        context = self.get_context(request)
        context["form_submission"] = form_submission
        response = render(
            request, self.get_landing_page_template(request), context
        )
        return response

    def data_to_dict(self, processed_data, request):
        """
        Converts processed form data into a dictionary suitable
        for rendering in a context.
        """
        dictionary = {}

        for key, value in processed_data.items():
            new_key = key.replace("-", "_")
            if isinstance(value, list):
                dictionary[new_key] = ", ".join(value)
            else:
                dictionary[new_key] = (
                    utils.attempt_protected_media_value_conversion(
                        request, value
                    )
                )

        return dictionary

    preview_modes = [
        ("form", _("Form")),
        ("landing", _("Thank you page")),
    ]

    def serve_preview(self, request, mode):
        if mode == "landing":
            request.is_preview = True
            return self.render_landing_page(request)

        return super().serve_preview(request, mode)

    def serve_submissions_list_view(self, request, *args, **kwargs):
        """
        Returns list submissions view for admin.

        `list_submissions_view_class` can be set to provide custom view class.
        Your class must be inherited from SubmissionsListView.
        """
        view = self.submissions_list_view_class.as_view()
        return view(request, form_page=self, *args, **kwargs)

    def get_form(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)

        if request.method == "POST":
            return form_class(request.POST, request.FILES, *args, **form_params)
        return form_class(*args, **form_params)

    def contains_spam(self, request):
        """
        Checks to see if the spam honeypot was filled out.
        """
        if request.POST.get("cr-decoy-comments", None):
            return True
        return False

    def process_spam_request(self, form, request):
        """
        Called when spam is found in the request.
        """
        messages.error(request, self.get_spam_message())
        logger.info(
            "Detected spam submission on page: {0}\n{1}".format(
                self.title, vars(request)
            )
        )

        return self.process_form_get(form, request)

    def get_spam_message(self):
        return _(
            "There was an error while processing your submission.  Please try again."
        )

    def process_form_post(self, form, request):
        if form.is_valid():
            processed_data = self.process_data(form, request)
            form_submission = self.get_submission_class()(
                form_data=processed_data,
                page=self,
            )
            self.process_form_submission(
                request=request,
                form=form,
                form_submission=form_submission,
                processed_data=processed_data,
            )
            return self.render_landing_page(request, form_submission)
        return self.process_form_get(form, request)

    def process_form_get(self, form, request):
        context = self.get_context(request)
        context["form"] = form
        response = render(request, self.get_template(request), context)
        return response

    def serve(self, request, *args, **kwargs):
        form = self.get_form(request, page=self, user=request.user)
        if request.method == "POST":
            if self.spam_protection and self.contains_spam(request):
                return self.process_spam_request(form, request)
            return self.process_form_post(form, request)
        return self.process_form_get(form, request)

    def get_preview_context(self, request, *args, **kwargs):
        """
        In preview mode, simlpy show a blank form but do not handle submissions.
        """
        ctx = super().get_preview_context(request, *args, **kwargs)
        ctx["form"] = self.get_form(request, page=self, user=request.user)
        return ctx


class CoderedFormPage(CoderedFormMixin, CoderedWebPage):
    """
    This is basically a clone of wagtail.contrib.forms.models.AbstractForm
    with changes in functionality and extending CoderedWebPage vs wagtailcore.Page.
    """

    class Meta:
        verbose_name = _("CodeRed Form Page")
        abstract = True

    template = "coderedcms/pages/form_page.html"
    miniview_template = "coderedcms/pages/form_page.mini.html"
    landing_page_template = "coderedcms/pages/form_page_landing.html"

    base_form_class = WagtailAdminFormPageForm

    form_builder = CoderedFormBuilder

    body_content_panels = (
        CoderedWebPage.body_content_panels
        + [
            InlinePanel("form_fields", label="Form fields"),
        ]
        + CoderedFormMixin.body_content_panels
        + [
            FormSubmissionsPanel(),
            InlinePanel("confirmation_emails", label=_("Confirmation Emails")),
        ]
    )

    settings_panels = (
        CoderedPage.settings_panels + CoderedFormMixin.settings_panels
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "landing_page_template"):
            name, ext = os.path.splitext(self.template)
            self.landing_page_template = name + "_landing" + ext

    def get_form_fields(self):
        """
        Form page expects `form_fields` to be declared.
        If you want to change backwards relation name,
        you need to override this method.
        """

        return self.form_fields.all()

    def get_data_fields(self):
        """
        Returns a list of tuples with (field_name, field_label).
        """

        data_fields = [
            ("submit_time", _("Submission date")),
        ]
        data_fields += [
            (field.clean_name, field.label) for field in self.get_form_fields()
        ]
        return data_fields

    def get_form_class(self):
        fb = self.form_builder(self.get_form_fields())
        return fb.get_form_class()

    def get_form_parameters(self):
        return {}

    def get_submission_class(self):
        """
        Returns submission class.

        You can override this method to provide custom submission class.
        Your class must be inherited from AbstractFormSubmission.
        """

        return FormSubmission


class CoderedSubmissionRevision(SubmissionRevision, models.Model):
    pass


class CoderedSessionFormSubmission(SessionFormSubmission):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUSES = (
        (INCOMPLETE, _("Not submitted")),
        (COMPLETE, _("Complete")),
        (REVIEWED, _("Under consideration")),
        (APPROVED, _("Approved")),
        (REJECTED, _("Rejected")),
    )
    status = models.CharField(
        max_length=10, choices=STATUSES, default=INCOMPLETE
    )

    def create_normal_submission(self, delete_self=True):
        submission_data = self.get_data()
        if "user" in submission_data:
            submission_data["user"] = str(submission_data["user"])
        submission = FormSubmission.objects.create(
            form_data=submission_data,
            page=self.page,
        )

        if delete_self:
            CoderedSubmissionRevision.objects.filter(
                submission_id=self.id
            ).delete()
            self.delete()

        return submission

    def render_email(self, value):
        return value

    def render_link(self, value):
        return "{0}{1}".format(crx_settings.CRX_PROTECTED_MEDIA_URL, value)

    def render_image(self, value):
        return "{0}{1}".format(crx_settings.CRX_PROTECTED_MEDIA_URL, value)

    def render_file(self, value):
        return "{0}{1}".format(crx_settings.CRX_PROTECTED_MEDIA_URL, value)


@receiver(post_save)
def create_submission_changed_revision(sender, **kwargs):
    if not issubclass(sender, SessionFormSubmission):
        return
    submission = kwargs["instance"]
    created = kwargs["created"]
    CoderedSubmissionRevision.create_from_submission(
        submission,
        (
            CoderedSubmissionRevision.CREATED
            if created
            else CoderedSubmissionRevision.CHANGED
        ),
    )


@receiver(post_delete)
def create_submission_deleted_revision(sender, **kwargs):
    if not issubclass(sender, CoderedSessionFormSubmission):
        return
    submission = kwargs["instance"]
    CoderedSubmissionRevision.create_from_submission(
        submission, SubmissionRevision.DELETED
    )


class CoderedStep(Step):
    def get_markups_and_bound_fields(self, form):
        for struct_child in self.form_fields:
            block = struct_child.block
            if isinstance(block, FormFieldBlock):
                struct_value = struct_child.value
                field_name = block.get_slug(struct_value)
                yield form[field_name], "field", struct_child
            else:
                yield mark_safe(struct_child), "markup"


class CoderedSteps(Steps):
    def __init__(self, page, request=None):
        self.page = page
        # TODO: Make it possible to change the `form_fields` attribute.
        self.form_fields = page.form_fields
        self.request = request
        has_steps = any(
            isinstance(struct_child.block, FormStepBlock)
            for struct_child in self.form_fields
        )
        if has_steps:
            steps = [
                CoderedStep(self, i, form_field)
                for i, form_field in enumerate(self.form_fields)
            ]
        else:
            steps = [CoderedStep(self, 0, self.form_fields)]
        super(Steps, self).__init__(steps)


class CoderedStreamFormMixin(StreamFormMixin):
    class Meta:
        abstract = True

    def get_steps(self, request=None):
        if not hasattr(self, "steps"):
            steps = CoderedSteps(self, request=request)
            if request is None:
                return steps
            self.steps = steps
        return self.steps

    @staticmethod
    def get_submission_class():
        return FormSubmission

    @staticmethod
    def get_session_submission_class():
        return CoderedSessionFormSubmission

    def get_submission(self, request):
        Submission = self.get_session_submission_class()
        if request.user.is_authenticated:
            user_submission = (
                Submission.objects.filter(user=request.user, page=self)
                .order_by("-pk")
                .first()
            )
            if user_submission is None:
                return Submission(user=request.user, page=self, form_data="[]")
            return user_submission

        # Custom code to ensure that anonymous users get a session key.
        if not request.session.session_key:
            request.session.create()

        user_submission = (
            Submission.objects.filter(
                session_key=request.session.session_key, page=self
            )
            .order_by("-pk")
            .first()
        )
        if user_submission is None:
            return Submission(
                session_key=request.session.session_key,
                page=self,
                form_data="[]",
            )
        return user_submission


class CoderedStreamFormPage(
    CoderedFormMixin, CoderedStreamFormMixin, CoderedWebPage
):
    class Meta:
        verbose_name = _("CodeRed Advanced Form Page")
        abstract = True

    template = "coderedcms/pages/stream_form_page.html"
    landing_page_template = "coderedcms/pages/form_page_landing.html"

    form_fields = StreamField(
        STREAMFORM_BLOCKS,
        use_json_field=True,
    )

    encoder = StreamFormJSONEncoder

    body_content_panels = (
        [FieldPanel("form_fields")]
        + CoderedFormMixin.body_content_panels
        + [InlinePanel("confirmation_emails", label=_("Confirmation Emails"))]
    )

    def process_form_post(self, form, request):
        if form.is_valid():
            is_complete = self.steps.update_data()
            if is_complete:
                submission = self.get_submission(request)
                self.process_form_submission(
                    request=request,
                    form=form,
                    form_submission=submission,
                    processed_data=submission.get_data(),
                )
                normal_submission = submission.create_normal_submission()
                return self.render_landing_page(request, normal_submission)
            return HttpResponseRedirect(self.url)
        return self.process_form_get(form, request)

    def process_form_get(self, form, request):
        return CoderedWebPage.serve(self, request)

    def get_form(self, request, *args, **kwargs):
        return self.get_context(request)["form"]

    def get_storage(self):
        return FileSystemStorage(
            location=crx_settings.CRX_PROTECTED_MEDIA_ROOT,
            base_url=crx_settings.CRX_PROTECTED_MEDIA_URL,
        )


class CoderedLocationPage(CoderedWebPage):
    """
    Location, suitable for store locations or help centers.
    """

    class Meta:
        verbose_name = _("CodeRed Location")
        abstract = True

    template = "coderedcms/pages/location_page.html"

    # Override body to provide simpler content
    body = StreamField(
        CONTENT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    address = models.TextField(blank=True, verbose_name=_("Address"))
    latitude = models.FloatField(
        blank=True, null=True, verbose_name=_("Latitude")
    )
    longitude = models.FloatField(
        blank=True, null=True, verbose_name=_("Longitude")
    )
    auto_update_latlng = models.BooleanField(
        default=True,
        verbose_name=_("Auto Update Latitude and Longitude"),
        help_text=_(
            "If checked, automatically update the latitude and longitude "
            "when the address is updated."
        ),
    )
    map_title = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Map Title"),
        help_text=_(
            "If this is filled out, this is the title that will be used on the map."
        ),
    )
    map_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Map Description"),
        help_text=_(
            "If this is filled out, this is the description that will be used on the map."
        ),
    )
    website = models.TextField(blank=True, verbose_name=_("Website"))
    phone_number = models.CharField(
        blank=True, max_length=255, verbose_name=_("Phone Number")
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("address"),
        FieldPanel("website"),
        FieldPanel("phone_number"),
    ]

    layout_panels = CoderedWebPage.layout_panels + [
        MultiFieldPanel(
            [
                FieldPanel("map_title"),
                FieldPanel("map_description"),
            ],
            heading=_("Map Layout"),
        ),
    ]

    settings_panels = CoderedWebPage.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("auto_update_latlng"),
                FieldPanel("latitude"),
                FieldPanel("longitude"),
            ],
            heading=_("Location Settings"),
        ),
    ]

    @property
    def geojson_name(self):
        return self.map_title or self.title

    @property
    def geojson_description(self):
        return self.map_description

    @property
    def render_pin_description(self):
        return render_to_string(
            "coderedcms/includes/map_pin_description.html", {"page": self}
        )

    @property
    def render_list_description(self):
        return render_to_string(
            "coderedcms/includes/map_list_description.html", {"page": self}
        )

    def to_geojson(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.longitude, self.latitude],
            },
            "properties": {
                "list_description": self.render_list_description,
                "pin_description": self.render_pin_description,
            },
        }

    def save(self, *args, **kwargs):
        if (
            self.auto_update_latlng
            and LayoutSettings.for_site(
                Site.objects.get(is_default_site=True)
            ).google_maps_api_key
        ):
            try:
                g = geocoder.google(
                    self.address,
                    key=LayoutSettings.for_site(
                        Site.objects.get(is_default_site=True)
                    ).google_maps_api_key,
                )
                self.latitude = g.latlng[0]
                self.longitude = g.latlng[1]
            except TypeError:
                # Raised if google denied the request
                pass

        return super(CoderedLocationPage, self).save(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["google_api_key"] = LayoutSettings.for_site(
            Site.objects.get(is_default_site=True)
        ).google_maps_api_key
        return context


class CoderedLocationIndexPage(CoderedWebPage):
    """
    Shows a map view of the children CoderedLocationPage.
    """

    class Meta:
        verbose_name = _("CodeRed Location Index Page")
        abstract = True

    template = "coderedcms/pages/location_index_page.html"

    index_show_subpages_default = True

    center_latitude = models.FloatField(
        null=True,
        blank=True,
        help_text=_("The default latitude you want the map set to."),
        default=0,
    )
    center_longitude = models.FloatField(
        null=True,
        blank=True,
        help_text=_("The default longitude you want the map set to."),
        default=0,
    )
    zoom = models.IntegerField(
        default=8,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1),
        ],
        help_text=_(
            "Requires API key to use zoom. "
            "1: World, 5: Landmass/continent, 10: City, 15: Streets, 20: Buildings"
        ),
    )

    layout_panels = CoderedWebPage.layout_panels + [
        MultiFieldPanel(
            [
                FieldPanel("center_latitude"),
                FieldPanel("center_longitude"),
                FieldPanel("zoom"),
            ],
            heading=_("Map Display"),
        ),
    ]

    def geojson_data(self, viewport=None):
        """
        function that will return all locations under this index as geoJSON compliant data.
        It is filtered by a latitude/longitude viewport if given.

        viewport is a string in the format of :
        'southwest.latitude,southwest.longitude|northeast.latitude,northeast.longitude'

        An example viewport that covers Cleveland, OH would look like this:
        '41.354912150983964,-81.95331736661791|41.663427748126935,-81.45206614591478'
        """
        qs = self.get_index_children().live()

        if viewport:
            southwest, northeast = viewport.split("|")
            southwest = [float(x) for x in southwest.split(",")]
            northeast = [float(x) for x in northeast.split(",")]

            qs = qs.filter(
                latitude__gte=southwest[0],
                latitude__lte=northeast[0],
                longitude__gte=southwest[1],
                longitude__lte=northeast[1],
            )

        return {
            "type": "FeatureCollection",
            "features": [location.to_geojson() for location in qs],
        }

    def serve(self, request, *args, **kwargs):
        data_format = request.GET.get("data-format", None)
        if data_format == "geojson":
            return self.serve_geojson(request, *args, **kwargs)
        return super().serve(request, *args, **kwargs)

    def serve_geojson(self, request, *args, **kwargs):
        viewport = request.GET.get("viewport", None)
        return JsonResponse(self.geojson_data(viewport=viewport))

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["google_api_key"] = LayoutSettings.for_site(
            Site.objects.get(is_default_site=True)
        ).google_maps_api_key
        return context
