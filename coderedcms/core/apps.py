from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoderedCoreAppConfig(AppConfig):
    name = 'coderedcms.core'
    label = 'coderedcmscore'
    verbose_name = _("Codered core")

    def ready(self):
        from wagtail.core.signal_handlers import register_signal_handlers
        register_signal_handlers()