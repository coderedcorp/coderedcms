"""
This code is largely copied or extended upon the now defunct
``wagtailimportexport`` package.

In the future we may want to build a more robust import/exporter for CSV files,
or simply deprecate all of this functionality.

See: https://github.com/torchbox/wagtail-import-export/
"""

import csv
import copy

from django import forms
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils.translation import gettext as _
from modelcluster.models import get_all_child_relations
from wagtail.admin.widgets import AdminPageChooser
from wagtail.models import Page

from coderedcms.forms import get_page_model_choices


class ImportPagesFromCSVFileForm(forms.Form):
    """
    Mostly copied from:
    https://github.com/torchbox/wagtail-import-export/blob/master/wagtailimportexport/forms.py#L29
    with addition of ``page_type``.
    """

    page_type = forms.ChoiceField(choices=get_page_model_choices)

    file = forms.FileField(label=_("File to import"))

    parent_page = forms.ModelChoiceField(
        queryset=Page.objects.all(),
        widget=AdminPageChooser(can_choose_root=True, show_edit_link=False),
        label=_("Destination parent page"),
        help_text=_("Imported pages will be created as children of this page."),
    )


def update_page_references(model, pages_by_original_id):
    """
    Copied from:
    https://github.com/torchbox/wagtail-import-export/blob/master/wagtailimportexport/importing.py#L67
    """
    for field in model._meta.get_fields():
        if isinstance(field, models.ForeignKey) and issubclass(
            field.related_model, Page
        ):
            linked_page_id = getattr(model, field.attname)
            try:
                # see if the linked page is one of the ones we're importing
                linked_page = pages_by_original_id[linked_page_id]
            except KeyError:
                # any references to pages outside of the import should be left unchanged
                continue

            # update fk to the linked page's new ID
            setattr(model, field.attname, linked_page.id)

    # update references within inline child models, including the ParentalKey pointing back
    # to the page
    for rel in get_all_child_relations(model):
        for child in getattr(model, rel.get_accessor_name()).all():
            # reset the child model's PK so that it will be inserted as a new record
            # rather than updating an existing one
            child.pk = None
            # update page references on the child model, including the ParentalKey
            update_page_references(child, pages_by_original_id)


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

    for page_record in import_data["pages"]:
        # build a base Page instance from the exported content
        # (so that we pick up its title and other core attributes)
        page = Page.from_serializable_data(page_record["content"])

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
        page_record["content"]["pk"] = page.pk

        pages_by_original_id[page.id] = page

    for page_record in import_data["pages"]:
        # Get the page model of the source page by app_label and model name
        # The content type ID of the source page is not in general the same
        # between the source and destination sites but the page model needs
        # to exist on both.
        # Raises LookupError exception if there is no matching model
        model = apps.get_model(page_record["app_label"], page_record["model"])

        specific_page = model.from_serializable_data(
            page_record["content"], check_fks=False, strict_fks=False
        )
        base_page = pages_by_original_id[specific_page.id]
        specific_page.base_page_ptr = base_page
        specific_page.__dict__.update(base_page.__dict__)
        specific_page.content_type = ContentType.objects.get_for_model(model)
        update_page_references(specific_page, pages_by_original_id)
        specific_page.save()

    return len(import_data["pages"])


def convert_csv_to_json(csv_file, page_type):
    pages_json = {"pages": []}
    app_label, klass = page_type.split(":")
    default_page_data = {
        "app_label": app_label,
        "content": {"pk": None},
        "model": klass,
    }

    pages_csv_dict = csv.DictReader(csv_file)
    for row in pages_csv_dict:
        page_dict = copy.deepcopy(default_page_data)
        page_dict["content"].update(row)
        pages_json["pages"].append(page_dict)
    return pages_json
