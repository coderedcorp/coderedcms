from django import forms

class ColorPickerWidget(forms.TextInput):
    input_type = 'color'
