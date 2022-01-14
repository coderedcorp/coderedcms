from django.db import models

from coderedcms.widgets import ColorPickerWidget
from django.forms.widgets import Textarea


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super().formfield(**kwargs)


class MonospaceField(models.TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = Textarea(attrs={
            "rows": 12,
            "class": "monospace",
            "spellcheck": "false",
        })
        return super().formfield(**kwargs)
