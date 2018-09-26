import os
import mimetypes

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render

from coderedcms.core import utils
from coderedcms.core.models import GeneralSettings
from coderedcms.core.settings import cr_settings


@login_required
def serve_protected_file(request, path):
    """
    Function that serves protected files uploaded from forms.
    """
    fullpath = os.path.join(cr_settings['PROTECTED_MEDIA_ROOT'], path)
    if os.path.isfile(fullpath):
        mimetype, encoding = mimetypes.guess_type(fullpath)
        with open(fullpath, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mimetype)
        if encoding:
            response["Content-Encoding"] = encoding

        return response
    else:
        raise Http404()


@login_required
def clear_cache(request):
    utils.clear_cache()
    return HttpResponse("Cache has been cleared.")


def robots(request):
    robots = GeneralSettings.for_site(request.site).robots
    return render(
        request,
        'robots.txt',
        {'robots': robots},
        content_type='text/plain'
    )
