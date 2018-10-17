from django import forms
from django.utils.safestring import mark_safe

class ColorPickerWidget(forms.TextInput):
    input_type = 'color'