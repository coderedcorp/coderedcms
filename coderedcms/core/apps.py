from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoderedCoreAppConfig(AppConfig):
    name = 'coderedcms.core'
    label = 'coderedcmscore'
    verbose_name = _("Codered core")