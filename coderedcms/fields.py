from django.db import models

from coderedcms.widgets import ColorPickerWidget
from django.forms.widgets import Textarea


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super(ColorField, self).formfield(**kwargs)

class ScriptField(models.TextField):
    def __init__(self, *args, **kwargs):
        super(ScriptField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = Textarea(attrs={
            'rows': 15,
            'cols': 10,
            'style': 'font-family:SFMono-Regular,Menlo,Monaco,Consolas,monospace;'
        })
        return super(ScriptField, self).formfield(**kwargs)
