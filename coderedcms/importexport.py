import csv
import copy

from django import forms
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from wagtail.core.models import Page

from wagtailimportexport.forms import ImportFromFileForm
from wagtailimportexport.importing import update_page_references

from coderedcms.forms import get_page_model_choices


class ImportPagesFromCSVFileForm(ImportFromFileForm):
    page_type = forms.ChoiceField(choices=get_page_model_choices)


@transaction.atomic()
def import_pages(import_data, parent_page):
    """
    Overwrite of the wagtailimportexport `import_page` function to handle generic csvs.
    The standard `import_pages` assumes that your pages will have a pk from the exported
    json files.  It does not facilitate the idea that the pages you import will be
    new pages.
    """

    pages_by_original_id = {}

    # First create the base Page records; these contain no foreign keys, so this allows us to
    # build a complete mapping from old IDs to new IDs before we go on to importing the
    # specific page models, which may require us to rewrite page IDs within foreign keys / rich
    # text / streamfields.
    page_content_type = ContentType.objects.get_for_model(Page)

    for page_record in import_data['pages']:
        # build a base Page instance from the exported content
        # (so that we pick up its title and other core attributes)
        page = Page.from_serializable_data(page_record['content'])

        # clear id and treebeard-related fields so that
        # they get reassigned when we save via add_child
        page.id = None
        page.path = None
        page.depth = None
        page.numchild = 0
        page.url_path = None
        page.content_type = page_content_type
        parent_page.add_child(instance=page)

        # Custom Code to add the new pk back into the original page record.
        page_record['content']['pk'] = page.pk

        pages_by_original_id[page.id] = page

    for page_record in import_data['pages']:
        # Get the page model of the source page by app_label and model name
        # The content type ID of the source page is not in general the same
        # between the source and destination sites but the page model needs
        # to exist on both.
        # Raises LookupError exception if there is no matching model
        model = apps.get_model(page_record['app_label'], page_record['model'])

        specific_page = model.from_serializable_data(
            page_record['content'],
            check_fks=False,
            strict_fks=False
        )
        base_page = pages_by_original_id[specific_page.id]
        specific_page.page_ptr = base_page
        specific_page.__dict__.update(base_page.__dict__)
        specific_page.content_type = ContentType.objects.get_for_model(model)
        update_page_references(specific_page, pages_by_original_id)
        specific_page.save()

    return len(import_data['pages'])


def convert_csv_to_json(csv_file, page_type):
    pages_json = {"pages": []}
    default_page_data = {"app_label": "website", "content": {"pk": None}, "model": page_type}

    pages_csv_dict = csv.DictReader(csv_file)
    for row in pages_csv_dict:
        page_dict = copy.deepcopy(default_page_data)
        page_dict['content'].update(row)
        pages_json['pages'].append(page_dict)
    return pages_json
