"""
Custom wagtail settings used by CodeRed CMS.
Settings are user-configurable on a per-site basis (multisite).
Global project or developer settings should be defined in coderedcms.settings.py .
"""

import json
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import HelpPanel, FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images import get_image_model_string

from coderedcms.settings import cr_settings


@register_setting(icon='fa-facebook-official')
class SocialMediaSettings(BaseSetting):
    """
    Social media accounts.
    """
    class Meta:
        verbose_name = _('Social Media')

    facebook = models.URLField(
        blank=True,
        verbose_name=_('Facebook'),
        help_text=_('Your Facebook page URL'),
    )
    twitter = models.URLField(
        blank=True,
        verbose_name=_('Twitter'),
        help_text=_('Your Twitter page URL'),
    )
    instagram = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Instagram'),
        help_text=_('Your Instagram username, without the @'),
    )
    youtube = models.URLField(
        blank=True,
        verbose_name=_('YouTube'),
        help_text=_('Your YouTube channel or user account URL'),
    )
    linkedin = models.URLField(
        blank=True,
        verbose_name=_('LinkedIn'),
        help_text=_('Your LinkedIn page URL'),
    )
    googleplus = models.URLField(
        blank=True,
        verbose_name=_('Google'),
        help_text=_('Your Google+ page or Google business listing URL'),
    )

    @property
    def twitter_handle(self):
        """
        Gets the handle of the twitter account from a URL.
        """
        return self.twitter.strip().strip('/').split('/')[-1]

    @property
    def social_json(self):
        """
        Returns non-blank social accounts as a JSON list.
        """
        socialist = [
            self.facebook,
            self.twitter,
            self.instagram,
            self.youtube,
            self.linkedin,
            self.googleplus,
        ]
        socialist = list(filter(None, socialist))
        return json.dumps(socialist)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('facebook'),
                FieldPanel('twitter'),
                FieldPanel('instagram'),
                FieldPanel('youtube'),
                FieldPanel('linkedin'),
                FieldPanel('googleplus'),
            ],
            _('Social Media Accounts'),
        )
    ]


@register_setting(icon='fa-desktop')
class LayoutSettings(BaseSetting):
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
        choices=cr_settings['FRONTEND_NAVBAR_COLOR_SCHEME_CHOICES'],
        default=cr_settings['FRONTEND_NAVBAR_COLOR_SCHEME_DEFAULT'],
        verbose_name=_('Navbar color scheme'),
        help_text=_('Optimizes text and other navbar elements for use with light or dark backgrounds.'),  # noqa
    )
    navbar_class = models.CharField(
        blank=True,
        max_length=255,
        default=cr_settings['FRONTEND_NAVBAR_CLASS_DEFAULT'],
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
        choices=cr_settings['FRONTEND_NAVBAR_COLLAPSE_MODE_CHOICES'],
        default=cr_settings['FRONTEND_NAVBAR_COLLAPSE_MODE_DEFAULT'],
        verbose_name=_('Collapse navbar menu'),
        help_text=_('Control on what screen sizes to show and collapse the navbar menu links.'),
    )
    navbar_format = models.CharField(
        blank=True,
        max_length=50,
        choices=cr_settings['FRONTEND_NAVBAR_FORMAT_CHOICES'],
        default=cr_settings['FRONTEND_NAVBAR_FORMAT_DEFAULT'],
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
        choices=cr_settings['FRONTEND_THEME_CHOICES'],
        default=cr_settings['FRONTEND_THEME_DEFAULT'],
        verbose_name=_('Theme variant'),
        help_text=cr_settings['FRONTEND_THEME_HELP'],
    )

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('logo'),
                ImageChooserPanel('favicon'),
            ],
            heading=_('Branding')
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
        MultiFieldPanel(
            [
                FieldPanel('frontend_theme'),
            ],
            heading=_('Theming')
        ),
    ]


@register_setting(icon='fa-google')
class AnalyticsSettings(BaseSetting):
    """
    Tracking and Google Analytics.
    """
    class Meta:
        verbose_name = _('Tracking')

    ga_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('GA Tracking ID'),
        help_text=_('Your Google Analytics tracking ID (begins with "UA-")'),
    )
    ga_track_button_clicks = models.BooleanField(
        default=False,
        verbose_name=_('Track button clicks'),
        help_text=_('Track all button clicks using Google Analytics event tracking. Event tracking details can be specified in each button’s advanced settings options.'),  # noqa
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('ga_tracking_id'),
                FieldPanel('ga_track_button_clicks'),
            ],
            heading=_('Google Analytics')
        )
    ]


@register_setting(icon='fa-universal-access')
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


@register_setting(icon='fa-line-chart')
class SeoSettings(BaseSetting):
    """
    Additional search engine optimization and meta tags
    that can be turned on or off.
    """
    class Meta:
        verbose_name = _('SEO')

    og_meta = models.BooleanField(
        default=True,
        verbose_name=_('Use OpenGraph Markup'),
        help_text=_('Show an optimized preview when linking to this site on Facebook, Linkedin, Twitter, and others. See http://ogp.me/.'),  # noqa
    )
    twitter_meta = models.BooleanField(
        default=True,
        verbose_name=_('Use Twitter Markup'),
        help_text=_('Shows content as a "card" when linking to this site on Twitter. See https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/abouts-cards.'),  # noqa
    )
    struct_meta = models.BooleanField(
        default=True,
        verbose_name=_('Use Structured Data'),
        help_text=_('Optimizes information about your organization for search engines. See https://schema.org/.'),  # noqa
    )
    amp_pages = models.BooleanField(
        default=True,
        verbose_name=_('Use AMP Pages'),
        help_text=_('Generates an alternate AMP version of Article pages that are preferred by search engines. See https://www.ampproject.org/'),  # noqa
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('og_meta'),
                FieldPanel('twitter_meta'),
                FieldPanel('struct_meta'),
                FieldPanel('amp_pages'),
                HelpPanel(content=_('If these settings are enabled, the corresponding values in each page’s SEO tab are used.')),  # noqa
            ],
            heading=_('Search Engine Optimization')
        )
    ]


@register_setting(icon='fa-puzzle-piece')
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


@register_setting(icon='fa-puzzle-piece')
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
