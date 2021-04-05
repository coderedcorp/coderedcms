# what imports do I need?

# from django.apps import apps
# from django.test import Client, TestCase
# from django.db.migrations.executor import MigrationExecutor
# from django.db import connection

# from wagtail.core.models import Site

# from coderedcms.models.wagtailsettings_models import (
#     LayoutSettings,
#     NavbarOrderable,
#     FooterOrderable
# )

# Set up

# class TestMigrations(TestCase):

#     @property
#     def app(self):
#         return apps.get_containing_app_config(type(self).__module__).name

#     migrate_from = None
#     migrate_to = None

# Need to create Site that has navbar and footer the current way
# Then run the migration and check if the navbar and footer was added to orderables
