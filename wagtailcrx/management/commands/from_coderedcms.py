from django.core.management.base import BaseCommand, CommandError



class Command(BaseCommand):
    help = "Converts core parts of a coderedcms 0.x project to wagtailcrx 1.x"

    def handle(self, *args, **options):
        # TODO - rename migrations in database from "coderedcms" to
        # "wagtailcrx". Confirmed this works OK.
