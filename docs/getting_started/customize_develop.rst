Developing your website
=======================


Page models
-------------

The django app ``website`` has been created with default models based on pre-built abstract
CodeRed CMS models. You can use these as-is, override existing fields and function, and add
custom fields to these models. After making a change to any of these models, be sure to run
``python manage.py makemigrations website`` and ``python manage.py migrate`` to apply the
database changes.


Hooks
-----

Building on the concept of wagtail hooks, there are some additional hooks in CodeRed CMS

is_request_cacheable
^^^^^^^^^^^^^^^^^^^^

This hook is provided by `wagtail-cache <https://github.com/coderedcorp/wagtail-cache>`_.
The callable passed into this hook should take a ``request`` argument, and return a ``bool``
indicating whether or not the response to this request should be cached (served from the cache
if it is already cached). Not returning, or returning anything other than a bool will not
affect the caching decision. For example::

    from wagtail.core import hooks

    @hooks.register('is_request_cacheable')
    def nocache_in_query(request, curr_cache_decision):
        # if the querystring contains a "nocache" key, return False to forcibly not cache.
        # otherwise, do not return to let the CMS decide how to cache.
        if 'nocache' in request.GET:
            return False


Default Language
----------------

To adjust the default language of a project, navigate to Project_Name/Project_Name/settings/base.py. Change both the
LANGUAGE_CODE setting and the LANGUAGES setting. For example::

        LANGUAGE_CODE = 'es'

        LANGUAGES = [
            ('es', _('Spanish'))
        ]

Note that these settings are both in use to communicate to the users' browser about the default language of the project.
This ensures that users requiring assistive technology have a smooth experience using the site. These settings do not,
on their own, translate or enable multiple languages on the project.

`For a full list of language codes, see this list from W3 Docs. <https://www.w3docs.com/learn-html/html-language-codes.html>`_


