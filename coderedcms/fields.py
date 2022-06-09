from django.db import models
from django.forms.widgets import Textarea
from wagtail.core.fields import StreamField

from coderedcms.widgets import ColorPickerWidget


class CoderedStreamField(StreamField):
    """
    An exact copy of the Wagtail StreamField, modified to NOT PRESERVE HISTORY
    in Django migrations.

    Since our StreamFields are generally huge, and we also let sites override
    the blocks in our concrete models dynamically, this creates a slew of
    migration problems (most commonly: a client overrides CODERED_FRONTEND_*,
    which changes a string used in a concrete model, which triggers a migration
    back in coderedcms). Eliminiating the blocks from the deconstructed
    StreamField allows us to have dynamic streamfields without breaking
    migrations or having to refactor the core concepts of this package.

    Internally, we should ALWAYS use CoderedStreamField on CONCRETE models,
    meaning models which are part of our package and saved to the database. For
    ABSTRACT models - meaning they are made concrete in the client site - we
    should continue to use Wagtail StreamField to keep things Wagtail-ish by
    default. The client may then decide to use CoderedStreamField if they are
    annoyed by the big migrations.

    CAVEAT EMPTOR:

    Client sites built with CRX may use this in place of the Wagtail
    StreamField, in order to avoid huge migration files. However, note that it
    will not be possible to mine data out of a CoderedStreamField during a
    migration (e.g. RunPython).

    Inspired by:
    https://cynthiakiser.com/blog/2022/01/06/trimming-wagtail-migration-cruft.html
    """
    def __init__(self, *args, **kwargs):
        """
        Patch init to work around django reconstruct not sending empty args.
        """
        # If we did not get an arg, pass an empty list through to the parent.
        if not args:
            args = [[]]
        return super().__init__(*args, **kwargs)

    def deconstruct(self):
        """
        Override to ignore any blocks within the StreamField when
        decustructing into a migration.

        The output should look something like this, regardless of how many
        blocks are nested within the StreamField::

            ("body", coderedcms.fields.CoderedStreamField([]))

        """
        name, path, block_types, kwargs = super().deconstruct()
        block_types = []
        return name, path, block_types, kwargs


class ColorField(models.CharField):
    """
    A CharField which uses the HTML5 color picker widget.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super().formfield(**kwargs)


class MonospaceField(models.TextField):
    """
    A TextField which renders as a large HTML textarea with monospace font.
    """
    def formfield(self, **kwargs):
        kwargs["widget"] = Textarea(attrs={
            "rows": 12,
            "class": "monospace",
            "spellcheck": "false",
        })
        return super().formfield(**kwargs)
