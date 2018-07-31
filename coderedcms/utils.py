from functools import wraps
from django.core.cache import caches
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.middleware.cache import CacheMiddleware
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from wagtail.core import hooks

from coderedcms.settings import cr_settings


def get_protected_media_link(request, path, render_link=False):
    if render_link:
        return mark_safe("<a href='{0}{1}'>{0}{1}</a>".format(request.build_absolute_uri('/')[:-1], path))
    return "{0}{1}".format(request.build_absolute_uri('/')[:-1], path)

def uri_validator(possible_uri):
    validate = URLValidator()
    try:
        validate(possible_uri)
        return True
    except ValidationError:
        return False

def attempt_protected_media_value_conversion(request, value):
    new_value = value
    try:
        if value.startswith(cr_settings['PROTECTED_MEDIA_URL']):
            new_value = get_protected_media_link(request, value)
    except AttributeError:
        pass
    return new_value

def clear_cache():
    if cr_settings['CACHE_PAGES']:
        cache = caches[cr_settings['CACHE_BACKEND']]
        cache.clear()

def cache_page(view_func):
    """
    Decorator that determines whether or not to cache a page or serve a cached page.
    """
    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        if cr_settings['CACHE_PAGES']:

            # check if request is cacheable
            request.is_preview = getattr(request, 'is_preview', False)
            is_cacheable = request.method in ('GET', 'HEAD') and not request.is_preview and not request.user.is_authenticated
            for fn in hooks.get_hooks('is_request_cacheable'):
                result = fn(request)
                if isinstance(result, bool):
                    is_cacheable = result

            if is_cacheable:
                cache = caches[cr_settings['CACHE_BACKEND']]
                djcache = CacheMiddleware(
                    cache_alias=cr_settings['CACHE_BACKEND'],
                    cache_timeout=cache.default_timeout, # override CacheMiddleware's default timeout
                    key_prefix=None
                )
                response = djcache.process_request(request)
                if response:
                    response['X-Crcms-Cache'] = 'hit'
                    return response

                # since we don't have a response at this point, run the view.
                response = view_func(request, *args, **kwargs)
                response['X-Crcms-Cache'] = 'miss'
                djcache.process_response(request, response)

                return response

        # as a fall-back, just run the view function.
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func

def seconds_to_readable(seconds):
    """
    Converts int seconds to a human readable string.
    """
    if seconds <= 0:
        return '{0} {1}'.format(str(seconds), _('seconds'))

    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)
    pretty_time = ''
    if days > 0:
        pretty_time += ' {0} {1}'.format(str(days), _('days') if days > 1 else _('day'))
    if hrs > 0:
        pretty_time += ' {0} {1}'.format(str(hrs), _('hours') if hrs > 1 else _('hour'))
    if mins > 0:
        pretty_time += ' {0} {1}'.format(str(mins), _('minutes') if mins > 1  else _('minute'))
    if secs > 0:
        pretty_time += ' {0} {1}'.format(str(secs), _('seconds') if secs > 1  else _('second'))
    return pretty_time