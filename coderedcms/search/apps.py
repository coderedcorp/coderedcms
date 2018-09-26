from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoderedSearchAppConfig(AppConfig):
    name = 'coderedcms.search'
    label = 'coderedcmssearch'
    verbose_name = _("Codered search")
