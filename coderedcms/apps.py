from django.apps import AppConfig


class CoderedcmsConfig(AppConfig):
    name = 'coderedcms'
    verbose_name = 'Wagtail CRX'
    # TODO: At some point in the future, change this to BigAutoField and create
    # the corresponding migration for concrete models in coderedcms.
    default_auto_field = 'django.db.models.AutoField'
