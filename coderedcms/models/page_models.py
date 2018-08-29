"""
Base and abstract pages used in CodeRed CMS.
"""

import json
import os
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    HelpPanel,
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface)
from wagtail.core.fields import StreamField
from wagtail.core.models import PageBase, Page, Site
from wagtail.core.utils import resolve_model_string
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.forms import WagtailAdminFormPageForm
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import FormSubmission
from wagtail.search import index

from coderedcms import schema, utils
from coderedcms.blocks import (
    CONTENT_STREAMBLOCKS,
    LAYOUT_STREAMBLOCKS,
    ContentWallBlock,
    OpenHoursBlock,
    StructuredDataActionBlock)
from coderedcms.forms import CoderedFormBuilder, CoderedSubmissionsListView
from coderedcms.models.wagtailsettings_models import GeneralSettings, LayoutSettings, SeoSettings
from coderedcms.settings import cr_settings


CODERED_PAGE_MODELS = []


def get_page_models():
    return CODERED_PAGE_MODELS


class CoderedPageMeta(PageBase):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if 'amp_template' not in dct:
            cls.amp_template = None
        if 'search_db_include' not in dct:
            cls.search_db_include = False
        if 'search_db_boost' not in dct:
            cls.search_db_boost = 0
        if 'search_filterable' not in dct:
            cls.search_filterable = False
        if 'search_name' not in dct:
            cls.search_name = cls._meta.verbose_name
        if 'search_name_plural' not in dct:
            cls.search_name_plural = cls._meta.verbose_name_plural
        if 'search_template' not in dct:
            cls.search_template = 'coderedcms/pages/search_result.html'
        if not cls._meta.abstract:
            CODERED_PAGE_MODELS.append(cls)


class CoderedPage(Page, metaclass=CoderedPageMeta):
    """
    General use page with caching, templating, and SEO functionality.
    All pages should inherit from this.
    """
    class Meta:
        verbose_name = _('CodeRed Page')

    # Do not allow this page type to be created in wagtail admin
    is_creatable = False

    # Templates
    # The page will render the following templates under certain conditions:
    #
    # template = ''
    # amp_template = ''
    # ajax_template = ''
    # search_template = ''


    ###############
    # Content fields
    ###############
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Cover image'),
    )


    ###############
    # Index fields
    ###############

    # Subclasses can override this to enabled index features by default.
    index_show_subpages_default = False

    # Subclasses can override this to query on a specific
    # page model, rather than the default wagtail Page.
    index_query_pagemodel = 'wagtailcore.Page'

    # Subclasses can override these fields to enable custom
    # ordering based on specific subpage fields.
    index_order_by_default = '-first_published_at'
    index_order_by_choices = (
        ('-first_published_at', _('Date first published, newest to oldest')),
        ('first_published_at', _('Date first published, oldest to newest')),
        ('-last_published_at', _('Date updated, newest to oldest')),
        ('last_published_at', _('Date updated, oldest to newest')),
        ('title', _('Title, alphabetical')),
        ('-title', _('Title, reverse alphabetical')),
    )

    index_show_subpages = models.BooleanField(
        default=index_show_subpages_default,
        verbose_name=_('Show list of child pages')
    )
    index_order_by = models.CharField(
        max_length=255,
        choices=index_order_by_choices,
        default=index_order_by_default,
        verbose_name=_('Order child pages by'),
    )
    index_num_per_page = models.PositiveIntegerField(
        default=10,
        verbose_name=_('Number per page'),
    )


    ###############
    # Layout fields
    ###############

    custom_template = models.CharField(
        blank=True,
        max_length=255,
        choices=None,
        verbose_name=_('Template')
    )


    ###############
    # SEO fields
    ###############

    og_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Open Graph preview image'),
        help_text=_('The image shown when linking to this page on social media. If blank, defaults to article cover image, or logo in Settings > Layout > Logo')
    )
    struct_org_type = models.CharField(
        default='',
        blank=True,
        max_length=255,
        choices=schema.SCHEMA_ORG_CHOICES,
        verbose_name=_('Organization type'),
        help_text=_('If blank, no structured data will be used on this page.')
    )
    struct_org_name = models.CharField(
        default='',
        blank=True,
        max_length=255,
        verbose_name=_('Organization name'),
        help_text=_('Leave blank to use the site name in Settings > Sites')
    )
    struct_org_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Organization logo'),
        help_text=_('Leave blank to use the logo in Settings > Layout > Logo')
    )
    struct_org_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Photo of Organization'),
        help_text=_('A photo of the facility. This photo will be cropped to 1:1, 4:3, and 16:9 aspect ratios automatically.')
    )
    struct_org_phone = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Telephone number'),
        help_text=_('Include country code for best results. For example: +1-216-555-8000')
    )
    struct_org_address_street = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Street address'),
        help_text=_('House number and street. For example, 55 Public Square Suite 1710')
    )
    struct_org_address_locality = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('City'),
        help_text=_('City or locality. For example, Cleveland')
    )
    struct_org_address_region = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('State'),
        help_text=_('State, province, county, or region. For example, OH')
    )
    struct_org_address_postal = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Postal code'),
        help_text=_('Zip or postal code. For example, 44113')
    )
    struct_org_address_country = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Country'),
        help_text=_('For example, USA. Two-letter ISO 3166-1 alpha-2 country code is also acceptible https://en.wikipedia.org/wiki/ISO_3166-1')
    )
    struct_org_geo_lat = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=8,
        verbose_name=_('Geographic latitude')
    )
    struct_org_geo_lng = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=8,
        verbose_name=_('Geographic longitude')
    )
    struct_org_hours = StreamField(
        [
            ('hours', OpenHoursBlock()),
        ],
        blank=True,
        verbose_name=_('Hours of operation')
    )
    struct_org_actions = StreamField(
        [
            ('actions', StructuredDataActionBlock())
        ],
        blank=True,
        verbose_name=_('Actions')
    )
    struct_org_extra_json = models.TextField(
        blank=True,
        verbose_name=_('Additional Organization markup'),
        help_text=_('Additional JSON-LD inserted into the Organization dictionary. Must be properties of https://schema.org/Organization or the selected organization type.')
    )


    ###############
    # Settings
    ###############

    content_walls = StreamField(
        [
            ('content_wall', ContentWallBlock())
        ],
        blank=True,
        verbose_name=_('Content Walls')
    )

    ###############
    # Search
    ###############

    search_fields = [
        index.SearchField('title', partial_match=True, boost=3),
        index.SearchField('seo_title', partial_match=True, boost=3),
        index.SearchField('search_description', boost=2),
        index.FilterField('title'),
        index.FilterField('id'),
        index.FilterField('live'),
        index.FilterField('owner'),
        index.FilterField('content_type'),
        index.FilterField('path'),
        index.FilterField('depth'),
        index.FilterField('locked'),
        index.FilterField('first_published_at'),
        index.FilterField('last_published_at'),
        index.FilterField('latest_revision_created_at'),
        index.FilterField('index_show_subpages'),
        index.FilterField('index_order_by'),
        index.FilterField('custom_template'),
    ]

    ###############
    # Panels
    ###############

    content_panels = (
        Page.content_panels +
        [
            ImageChooserPanel('cover_image'),
        ]
    )

    layout_panels = [
        MultiFieldPanel(
            [
                FieldPanel('custom_template')
            ],
            heading=_('Visual Design')
        ),
        MultiFieldPanel(
            [
                FieldPanel('index_show_subpages'),
                FieldPanel('index_num_per_page'),
                FieldPanel('index_order_by'),
            ],
            heading=_('Show Child Pages')
        )
    ]

    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('seo_title'),
                FieldPanel('search_description'),
                ImageChooserPanel('og_image'),
            ],
            _('Page Meta Data')
        ),
        MultiFieldPanel(
            [
                HelpPanel(
                    heading=_('About Organization Structured Data'),
                    content=_("""The fields below help define brand, contact, and storefront
                    information to search engines. This information should be filled out on
                    the site’s root page (Home Page). If your organization has multiple locations,
                    then also fill this info out on each location page using that particular
                    location’s info."""),
                ),
                FieldPanel('struct_org_type'),
                FieldPanel('struct_org_name'),
                ImageChooserPanel('struct_org_logo'),
                ImageChooserPanel('struct_org_image'),
                FieldPanel('struct_org_phone'),
                FieldPanel('struct_org_address_street'),
                FieldPanel('struct_org_address_locality'),
                FieldPanel('struct_org_address_region'),
                FieldPanel('struct_org_address_postal'),
                FieldPanel('struct_org_address_country'),
                FieldPanel('struct_org_geo_lat'),
                FieldPanel('struct_org_geo_lng'),
                StreamFieldPanel('struct_org_hours'),
                StreamFieldPanel('struct_org_actions'),
                FieldPanel('struct_org_extra_json'),
            ],
            _('Structured Data - Organization')
        ),
    ]

    settings_panels = (
        Page.settings_panels + 
        [
            StreamFieldPanel('content_walls'),
        ]
    )

    def __init__(self, *args, **kwargs):
        """
        Inject custom choices and defalts into the form fields
        to enable customization by subclasses.
        """
        super().__init__(*args, **kwargs)

        klassname = self.__class__.__name__.lower()
        template_choices = cr_settings['FRONTEND_TEMPLATES_PAGES'].get('*', ()) + \
                           cr_settings['FRONTEND_TEMPLATES_PAGES'].get(klassname, ())


        self._meta.get_field('index_order_by').choices = self.index_order_by_choices
        self._meta.get_field('custom_template').choices = template_choices
        if not self.id:
            self.index_order_by = self.index_order_by_default
            self.index_show_subpages = self.index_show_subpages_default

    @classmethod
    def get_edit_handler(cls):
        """
        Override to "lazy load" the panels overriden by subclasses.
        """
        return TabbedInterface([
            ObjectList(cls.content_panels, heading='Content'),
            ObjectList(cls.layout_panels, heading='Layout'),
            ObjectList(cls.promote_panels, heading='SEO', classname="seo"),
            ObjectList(cls.settings_panels, heading='Settings', classname="settings"),
        ]).bind_to_model(cls)

    def get_struct_org_name(self):
        """
        Gets org name for sturctured data using a fallback.
        """
        if self.struct_org_name:
            return self.struct_org_name
        return self.get_site().site_name

    def get_struct_org_logo(self):
        """
        Gets logo for structured data using a fallback.
        """
        if self.struct_org_logo:
            return self.struct_org_logo
        else:
            layout_settings = LayoutSettings.for_site(self.get_site())
            if layout_settings.logo:
                return layout_settings.logo
        return None

    def get_template(self, request, *args, **kwargs):
        """
        Override parent to serve different templates based on querystring.
        """
        if 'amp' in request.GET and hasattr(self, 'amp_template'):
            seo_settings = SeoSettings.for_site(request.site)
            if seo_settings.amp_pages:
                if request.is_ajax():
                    return self.ajax_template or self.amp_template
                return self.amp_template

        if self.custom_template:
            return self.custom_template

        return super(CoderedPage, self).get_template(request, args, kwargs)

    def get_index_children(self):
        """
        Override to return query of subpages as defined by `index_` variables.
        """
        if self.index_query_pagemodel:
            querymodel = resolve_model_string(self.index_query_pagemodel, self._meta.app_label)
            return querymodel.objects.child_of(self).order_by(self.index_order_by)

        return super().get_children().live()

    def get_content_walls(self, check_child_setting=True):
        current_content_walls = []
        if check_child_setting:
            for wall in self.content_walls:
                content_wall = wall.value
                if wall.value['show_content_wall_on_children']:
                    current_content_walls.append(wall.value)
        else:
            current_content_walls = self.content_walls
            
        try:
            return list(current_content_walls) + self.get_parent().specific.get_content_walls()
        except AttributeError:
            return list(current_content_walls)

    def get_context(self, request, *args, **kwargs):
        """
        Add child pages and paginated child pages to context.
        """
        context = super().get_context(request)

        if self.index_show_subpages:
            all_children = self.get_index_children()
            paginator = Paginator(all_children, self.index_num_per_page)
            page = request.GET.get('p', 1)
            try:
                paged_children = paginator.page(page)
            except:
                paged_children = paginator.page(1)

            context['index_paginated'] = paged_children
            context['index_children'] = all_children
        context['content_walls'] = self.get_content_walls(check_child_setting=False)
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
        verbose_name = _('CodeRed Web Page')
        abstract = True

    template = 'coderedcms/pages/web_page.html'

    # Child pages should override based on what blocks they want in the body.
    # Default is LAYOUT_STREAMBLOCKS which is the fullest editor experience.
    body = StreamField(LAYOUT_STREAMBLOCKS, null=True, blank=True)

    # Search fields
    search_fields = (
        CoderedPage.search_fields +
        [index.SearchField('body')]
    )

    # Panels
    content_panels = (
        CoderedPage.content_panels +
        [StreamFieldPanel('body'),]
    )

    @property
    def body_preview(self):
        """
        A shortened, non-HTML version of the body.
        """
        # add spaces between tags for legibility
        body = str(self.body).replace('>', '> ')
        # strip tags
        body = strip_tags(body)
        # truncate and add ellipses
        return body[:200] + "..."


class CoderedArticlePage(CoderedWebPage):
    """
    Article, suitable for news or blog content.
    """
    class Meta:
        verbose_name = _('CodeRed Article')
        abstract = True

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'

    # Override body to provide simpler content
    body = StreamField(CONTENT_STREAMBLOCKS, null=True, blank=True)

    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Caption'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        related_name='articles',
        verbose_name=_('Author'),
    )
    author_display = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Display author as'),
        help_text=_('Override how the author’s name displays on this article.'),
    )
    date_display = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Display publish date'),
    )

    def get_author_name(self):
        """
        Gets author name using a fallback.
        """
        if self.author_display:
            return self.author_display
        if self.author:
            return self.author.get_full_name()
        return ''

    def get_pub_date(self):
        """
        Gets published date.
        """
        if self.date_display:
            return self.date_display
        return ''

    def get_description(self):
        """
        Gets the description using a fallback.
        """
        if self.search_description:
            return self.search_description
        if self.caption:
            return self.caption
        if self.body_preview:
            return self.body_preview
        return ''

    search_fields = (
        CoderedWebPage.search_fields +
        [
            index.SearchField('caption', boost=2),
            index.FilterField('author'),
            index.FilterField('author_display'),
            index.FilterField('date_display'),
        ]
    )

    content_panels = (
        CoderedWebPage.content_panels +
        [
            MultiFieldPanel(
                [
                    FieldPanel('caption'),
                ],
                _('Additional Content')
            ),
            MultiFieldPanel(
                [
                    FieldPanel('author'),
                    FieldPanel('author_display'),
                    FieldPanel('date_display'),
                ],
                _('Publication Info')
            )
        ]
    )


class CoderedArticleIndexPage(CoderedWebPage):
    """
    Shows a list of article sub-pages.
    """
    class Meta:
        verbose_name = _('CodeRed Article Index Page')
        abstract = True

    template = 'coderedcms/pages/article_index_page.html'

    index_show_subpages_default = True

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
                heading=_('Child page display')
            ),
        ]
    )


class CoderedFormPage(CoderedWebPage):
    """
    This is basically a clone of wagtail.contrib.forms.models.AbstractForm
    with changes in functionality and extending CoderedWebPage vs wagtailcore.Page.
    """
    class Meta:
        verbose_name = _('CodeRed Form Page')
        abstract = True

    template = 'coderedcms/pages/form_page.html'
    landing_page_template = 'coderedcms/pages/form_page_landing.html'

    base_form_class = WagtailAdminFormPageForm

    form_builder = CoderedFormBuilder

    submissions_list_view_class = CoderedSubmissionsListView

    ### Custom codered fields

    to_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Email form submissions to'),
        help_text=_('Optional - email form submissions to this address. Separate multiple addresses by comma.')
    )
    subject = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Subject'),
    )
    save_to_database = models.BooleanField(
        default=True,
        verbose_name=_('Save form submissions'),
        help_text=_('Submissions are saved to database and can be exported at any time.')
    )
    thank_you_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Thank you page'),
        help_text=_('The page users are redirected to after submitting the form.'),
    )
    button_text = models.CharField(
        max_length=255,
        default=_('Submit'),
        verbose_name=_('Button text'),
    )
    button_style = models.CharField(
        blank=True,
        choices=cr_settings['FRONTEND_BTN_STYLE_CHOICES'],
        default=cr_settings["FRONTEND_BTN_STYLE_DEFAULT"],
        max_length=255,
        verbose_name=_('Button style'),
    )
    button_size = models.CharField(
        blank=True,
        choices=cr_settings['FRONTEND_BTN_SIZE_CHOICES'],
        default=cr_settings["FRONTEND_BTN_SIZE_DEFAULT"],
        max_length=255,
        verbose_name=_('Button Size'),
    )
    button_css_class = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Button CSS class'),
        help_text=_('Custom CSS class applied to the submit button.'),
    )
    form_css_class = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Form CSS Class'),
        help_text=_('Custom CSS class applied to <form> element.'),
    )
    form_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Form ID'),
        help_text=_('Custom ID applied to <form> element.'),
    )
    form_golive_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Form go live date/time'),
        help_text=_('Date and time when the FORM goes live on the page.'),
    )
    form_expire_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Form expiry date/time'),
        help_text=_('Date and time when the FORM will no longer be available on the page.'),
    )

    content_panels = (
        CoderedWebPage.content_panels +
        [
            FormSubmissionsPanel(),
            InlinePanel('form_fields', label="Form fields"),
            MultiFieldPanel(
                [
                    PageChooserPanel('thank_you_page'),
                    FieldPanel('button_text'),
                    FieldPanel('button_style'),
                    FieldPanel('button_size'),
                    FieldPanel('button_css_class'),
                    FieldPanel('form_css_class'),
                    FieldPanel('form_id'),
                ],
                _('Form Settings')
            ),
            MultiFieldPanel(
                [
                    FieldPanel('save_to_database'),
                    FieldPanel('to_address'),
                    FieldPanel('subject'),
                ],
                _('Form Submissions')
            ),
            InlinePanel('confirmation_emails', label=_('Confirmation Emails'))
        ]
    )

    settings_panels = (
        CoderedPage.settings_panels +
        [
            MultiFieldPanel(
                [
                    FieldRowPanel(
                        [
                            FieldPanel('form_golive_at'),
                            FieldPanel('form_expire_at'),
                        ],
                        classname='label-above',
                    ),
                ],
                _('Form Scheduled Publishing'),
            )
        ]
    )

    @property
    def form_live(self):
        """
        A boolean on whether or not the <form> element should be shown on the page.
        """
        return (self.form_golive_at is None or self.form_golive_at <= timezone.now()) and \
               (self.form_expire_at is None or self.form_expire_at >= timezone.now())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'landing_page_template'):
            name, ext = os.path.splitext(self.template)
            self.landing_page_template = name + '_landing' + ext

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
            ('submit_time', _('Submission date')),
        ]
        data_fields += [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        return data_fields

    def get_form_class(self):
        fb = self.form_builder(self.get_form_fields())
        return fb.get_form_class()

    def get_form_parameters(self):
        return {}

    def get_form(self, *args, **kwargs):
        form_class = self.get_form_class()
        form_params = self.get_form_parameters()
        form_params.update(kwargs)

        return form_class(*args, **form_params)

    def get_landing_page_template(self, request, *args, **kwargs):
        return self.landing_page_template

    def get_submission_class(self):
        """
        Returns submission class.

        You can override this method to provide custom submission class.
        Your class must be inherited from AbstractFormSubmission.
        """

        return FormSubmission

    def process_form_submission(self, request, form):
        """
        Accepts form instance with submitted data, user and page.
        Creates submission instance.

        You can override this method if you want to have custom creation logic.
        For example, if you want to save reference to a user.
        """
        processed_data = {}

        # Handle file uploads
        for key, val in form.cleaned_data.items():
            if type(val) == InMemoryUploadedFile or type(val) == TemporaryUploadedFile:
                # Save the file and get its URL
                file_system = FileSystemStorage(
                    location=cr_settings['PROTECTED_MEDIA_ROOT'],
                    base_url=cr_settings['PROTECTED_MEDIA_URL']
                )
                filename = file_system.save(file_system.get_valid_name(val.name), val)
                processed_data[key] = file_system.url(filename)
            else:
                processed_data[key] = val

        # Get submission
        form_submission = self.get_submission_class()(
            form_data=json.dumps(processed_data, cls=DjangoJSONEncoder),
            page=self,
        )

        # Save to database
        if self.save_to_database:
            form_submission.save()

        # Send the mails
        if self.to_address:
            self.send_summary_mail(request, form, processed_data)

        if self.confirmation_emails:
            for email in self.confirmation_emails.all():
                from_address = email.from_address

                if from_address == '':
                    from_address = GeneralSettings.for_site(request.site).from_email_address

                template_body = Template(email.body)
                template_to = Template(email.to_address)
                template_from_email = Template(from_address)
                template_cc = Template(email.cc_address)
                template_bcc = Template(email.bcc_address)
                template_subject = Template(email.subject)
                context = Context(self.data_to_dict(processed_data))

                message = EmailMessage(
                    body=template_body.render(context),
                    to=template_to.render(context).split(','),
                    from_email=template_from_email.render(context),
                    cc=template_cc.render(context).split(','),
                    bcc=template_bcc.render(context).split(','),
                    subject=template_subject.render(context),
                )

                message.content_subtype = 'html'
                message.send()

        return processed_data

    def send_summary_mail(self, request, form, processed_data):
        """
        Sends a form submission summary email.
        """
        addresses = [x.strip() for x in self.to_address.split(',')]
        content = []
        for field in form:
            value = processed_data[field.name]
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{0}: {1}'.format(field.label, utils.attempt_protected_media_value_conversion(request, value)))
        content = '\n'.join(content)
        send_mail(
            self.subject,
            content,
            GeneralSettings.for_site(Site.objects.get(is_default_site=True)).from_email_address,
            addresses
        )

    def data_to_dict(self, processed_data):
        """
        Converts processed form data into a dictionary suitable
        for rendering in a context.
        """
        dictionary = {}

        for key, value in processed_data.items():
            dictionary[key.replace('-', '_')] = value
            if isinstance(value, list):
                dictionary[key] = ', '.join(value)

        return dictionary

    def render_landing_page(self, request, *args, form_submission=None, **kwargs):
        """
        Renders the landing page.

        You can override this method to return a different HttpResponse as
        landing page. E.g. you could return a redirect to a separate page.
        """
        if self.thank_you_page:
            return redirect(self.thank_you_page.url)

        context = self.get_context(request)
        context['form_submission'] = form_submission
        return render(
            request,
            self.get_landing_page_template(request),
            context
        )

    def serve_submissions_list_view(self, request, *args, **kwargs):
        """
        Returns list submissions view for admin.

        `list_submissions_view_class` can bse set to provide custom view class.
        Your class must be inherited from SubmissionsListView.
        """
        view = self.submissions_list_view_class.as_view()
        return view(request, form_page=self, *args, **kwargs)

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, request.FILES, page=self, user=request.user)

            if form.is_valid():
                form_submission = self.process_form_submission(request, form)
                return self.render_landing_page(request, form_submission, *args, **kwargs)
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )

    preview_modes = [
        ('form', _('Form')),
        ('landing', _('Thank you page')),
    ]

    def serve_preview(self, request, mode):
        if mode == 'landing':
            request.is_preview = True
            return self.render_landing_page(request)

        return super().serve_preview(request, mode)
