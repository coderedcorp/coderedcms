"""
Custom wagtail settings used by Wagtail CRX.
Settings are user-configurable on a per-site basis (multisite).
Global project or developer settings should be defined in coderedcms.settings.py .
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, HelpPanel, MultiFieldPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images import get_image_model_string
from coderedcms.fields import MonospaceField
from coderedcms.settings import crx_settings
from coderedcms.models.snippet_models import Navbar, Footer


@register_setting(icon='cr-desktop')
class LayoutSettings(ClusterableModel, BaseSetting):
    """
    Branding, navbar, and theme settings.
    """
    class Meta:
        verbose_name = _('Layout')

    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Logo'),
        help_text=_('Brand logo used in the navbar and throughout the site')
    )
    favicon = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='favicon',
        verbose_name=_('Favicon'),
    )
    navbar_color_scheme = models.CharField(
        blank=True,
        max_length=50,
        choices=None,
        default='',
        verbose_name=_('Navbar color scheme'),
        help_text=_('Optimizes text and other navbar elements for use with light or dark backgrounds.'),  # noqa
    )
    navbar_class = models.CharField(
        blank=True,
        max_length=255,
        default='',
        verbose_name=_('Navbar CSS class'),
        help_text=_('Custom classes applied to navbar e.g. "bg-light", "bg-dark", "bg-primary".'),
    )
    navbar_fixed = models.BooleanField(
        default=False,
        verbose_name=_('Fixed navbar'),
        help_text=_('Fixed navbar will remain at the top of the page when scrolling.'),
    )
    navbar_wrapper_fluid = models.BooleanField(
        default=True,
        verbose_name=_('Full width navbar'),
        help_text=_('The navbar will fill edge to edge.'),
    )
    navbar_content_fluid = models.BooleanField(
        default=False,
        verbose_name=_('Full width navbar contents'),
        help_text=_('Content within the navbar will fill edge to edge.'),
    )
    navbar_collapse_mode = models.CharField(
        blank=True,
        max_length=50,
        choices=None,
        default='',
        verbose_name=_('Collapse navbar menu'),
        help_text=_('Control on what screen sizes to show and collapse the navbar menu links.'),
    )
    navbar_format = models.CharField(
        blank=True,
        max_length=50,
        choices=None,
        default='',
        verbose_name=_('Navbar format'),
    )
    navbar_search = models.BooleanField(
        default=True,
        verbose_name=_('Search box'),
        help_text=_('Show search box in navbar')
    )
    frontend_theme = models.CharField(
        blank=True,
        max_length=50,
        choices=None,
        default='',
        verbose_name=_('Theme variant'),
    )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('logo'),
                ImageChooserPanel('favicon'),
            ],
            heading=_('Branding')
        ),
        InlinePanel(
            'site_navbar',
            help_text=_('Choose one or more navbars for your site.'),
            heading=_('Site Navbars')
        ),
        MultiFieldPanel(
            [
                FieldPanel('navbar_color_scheme'),
                FieldPanel('navbar_class'),
                FieldPanel('navbar_fixed'),
                FieldPanel('navbar_wrapper_fluid'),
                FieldPanel('navbar_content_fluid'),
                FieldPanel('navbar_collapse_mode'),
                FieldPanel('navbar_format'),
                FieldPanel('navbar_search'),
            ],
            heading=_('Site Navbar Layout')
        ),
        InlinePanel(
            'site_footer',
            help_text=_('Choose one or more footers for your site.'),
            heading=_('Site Footers')
        ),
        MultiFieldPanel(
            [
                FieldPanel('frontend_theme'),
            ],
            heading=_('Theming')
        ),
    ]

    def __init__(self, *args, **kwargs):
        """
        Inject custom choices and defaults into the form fields
        to enable customization of settings without causing migration issues.
        """
        super().__init__(*args, **kwargs)
        # Set choices dynamically.
        self._meta.get_field('frontend_theme').choices = (
            crx_settings.CRX_FRONTEND_THEME_CHOICES
        )
        self._meta.get_field('navbar_collapse_mode').choices = (
            crx_settings.CRX_FRONTEND_NAVBAR_COLLAPSE_MODE_CHOICES
        )
        self._meta.get_field('navbar_color_scheme').choices = (
            crx_settings.CRX_FRONTEND_NAVBAR_COLOR_SCHEME_CHOICES
        )
        self._meta.get_field('navbar_format').choices = (
            crx_settings.CRX_FRONTEND_NAVBAR_FORMAT_CHOICES
        )
        # Set default dynamically.
        if not self.id:
            self.frontend_theme = crx_settings.CRX_FRONTEND_THEME_DEFAULT
            self.navbar_class = crx_settings.CRX_FRONTEND_NAVBAR_CLASS_DEFAULT
            self.navbar_collapse_mode = crx_settings.CRX_FRONTEND_NAVBAR_COLLAPSE_MODE_DEFAULT
            self.navbar_color_scheme = crx_settings.CRX_FRONTEND_NAVBAR_COLOR_SCHEME_DEFAULT
            self.navbar_format = crx_settings.CRX_FRONTEND_NAVBAR_FORMAT_DEFAULT


class NavbarOrderable(Orderable, models.Model):
    navbar_chooser = ParentalKey(
        LayoutSettings,
        related_name="site_navbar",
        verbose_name=_('Site Navbars')
    )
    navbar = models.ForeignKey(
        Navbar,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("navbar")
    ]


class FooterOrderable(Orderable, models.Model):
    footer_chooser = ParentalKey(
        LayoutSettings,
        related_name="site_footer",
        verbose_name=_('Site Footers')
    )
    footer = models.ForeignKey(
        Footer,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("footer")
    ]


@register_setting(icon='cr-google')
class AnalyticsSettings(BaseSetting):
    """
    Tracking and Google Analytics.
    """
    class Meta:
        verbose_name = _('Tracking')

    ga_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('UA Tracking ID'),
        help_text=_('Your Google "Universal Analytics" tracking ID (begins with "UA-")'),
    )
    ga_g_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('G Tracking ID'),
        help_text=_('Your Google Analytics 4 tracking ID (begins with "G-")'),
    )
    ga_track_button_clicks = models.BooleanField(
        default=False,
        verbose_name=_('Track button clicks'),
        help_text=_('Track all button clicks using Google Analytics event tracking. Event tracking details can be specified in each button’s advanced settings options.'),  # noqa
    )
    gtm_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Google Tag Manager ID'),
        help_text=_('Begins with "GTM-"'),
    )
    head_scripts = MonospaceField(
        blank=True,
        null=True,
        verbose_name=_('<head> tracking scripts'),
        help_text=_('Add tracking scripts between the <head> tags.'),
    )
    body_scripts = MonospaceField(
        blank=True,
        null=True,
        verbose_name=_('<body> tracking scripts'),
        help_text=_('Add tracking scripts toward closing <body> tag.'),
    )

    panels = [
        HelpPanel(
            heading=_('Know your tracking'),
            content=_(
                '<h3><b>Which tracking IDs do I need?</b></h3>'
                '<p>Before adding tracking to your site, '
                '<a href="https://docs.coderedcorp.com/wagtail-crx/how_to/add_tracking_scripts.html" '  # noqa
                'target="_blank">read about the difference between UA, G, GTM, '
                'and other tracking IDs</a>.</p>'
            ),
        ),
        MultiFieldPanel(
            [
                FieldPanel('ga_tracking_id'),
                FieldPanel('ga_g_tracking_id'),
                FieldPanel('ga_track_button_clicks'),
            ],
            heading=_('Google Analytics'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('gtm_id'),
            ],
            heading=_('Google Tag Manager'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('head_scripts'),
                FieldPanel('body_scripts'),
            ],
            heading=_('Other Tracking Scripts')
        )
    ]


@register_setting(icon='cr-universal-access')
class ADASettings(BaseSetting):
    """
    Accessibility related options.
    """
    class Meta:
        verbose_name = 'Accessibility'

    skip_navigation = models.BooleanField(
        default=False,
        verbose_name=_('Show skip navigation link'),
        help_text=_('Shows a "Skip Navigation" link above the navbar that takes you directly to the main content.'),  # noqa
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('skip_navigation'),
            ],
            heading=_('Accessibility')
        )
    ]


@register_setting(icon='cog')
class GeneralSettings(BaseSetting):
    """
    Various site-wide settings. A good place to put
    one-off settings that don't belong anywhere else.
    """

    from_email_address = models.CharField(

        blank=True,
        max_length=255,
        verbose_name=_('From email address'),
        help_text=_('The default email address this site appears to send from. For example: "sender@example.com" or "Sender Name <sender@example.com>" (without quotes)'),  # noqa
    )
    search_num_results = models.PositiveIntegerField(
        default=10,
        verbose_name=_('Number of results per page'),
    )
    external_new_tab = models.BooleanField(
        default=False,
        verbose_name=_('Open all external links in new tab')
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('from_email_address'),
            ],
            _('Email')
        ),
        MultiFieldPanel(
            [
                FieldPanel('search_num_results'),
            ],
            _('Search Settings')
        ),
        MultiFieldPanel(
            [
                FieldPanel('external_new_tab'),
            ],
            _('Links')
        ),
    ]

    class Meta:
        verbose_name = _('General')


@register_setting(icon='cr-puzzle-piece')
class GoogleApiSettings(BaseSetting):
    """
    Settings for Google API services.
    """
    class Meta:
        verbose_name = _('Google API')

    google_maps_api_key = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Google Maps API Key'),
        help_text=_('The API Key used for Google Maps.')
    )


@register_setting(icon='cr-puzzle-piece')
class MailchimpApiSettings(BaseSetting):
    """
    Settings for Mailchimp API services.
    """
    class Meta:
        verbose_name = _('Mailchimp API')

    mailchimp_api_key = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Mailchimp API Key'),
        help_text=_('The API Key used for Mailchimp.')
    )
