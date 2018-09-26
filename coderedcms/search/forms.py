from django import forms
from django.utils.translation import ugettext_lazy as _

class SearchForm(forms.Form):
    s = forms.CharField(
        max_length=255,
        required=False,
        label=_('Search'),
    )
    t = forms.CharField(
        widget=forms.HiddenInput,
        max_length=255,
        required=False,
        label=_('Page type'),
    )
