from django import template
from wagtail.models import Site

from website.models import Footer
from website.models import Navbar


register = template.Library()


@register.simple_tag(takes_context=True)
def get_website_navbars(context):
    """Get the navbars for the current site.

    Args:
        context: The template context which contains the current request

    Returns:
        QuerySet: Navbar queryset filtered by the current site, or all navbars if fallback conditions are met
    """
    try:
        # Get the current request from context
        request = context['request']
        # Get the current site from the request
        current_site = Site.find_for_request(request)
        # Get navbars associated with the current site, if any
        site_navbars = Navbar.objects.filter(site=current_site)

        return site_navbars

    except (KeyError, AttributeError):
        # Fallback to returning all navbars if we can't determine the current site
        return Navbar.objects.all()


@register.simple_tag(takes_context=True)
def get_website_footers(context):
    """Get the footers for the current site.

    Args:
        context: The template context which contains the current request

    Returns:
        QuerySet: Footer queryset filtered by the current site, or all footers if fallback conditions are met
    """
    try:
        # Get the current request from context
        request = context['request']
        # Get the current site from the request
        current_site = Site.find_for_request(request)
        # Get footers associated with the current site, if any
        site_footers = Footer.objects.filter(site=current_site)

        return site_footers

    except (KeyError, AttributeError):
        # Fallback to returning all footers if we can't determine the current site
        return Footer.objects.all()
