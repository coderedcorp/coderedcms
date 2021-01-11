"""
JSON and meta-data blocks, primarily used for SEO purposes.
"""

import json
from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.core import blocks

from coderedcms import schema

from .base_blocks import MultiSelectBlock


class OpenHoursValue(blocks.StructValue):
    """
    Renders selected days as a json list.
    """
    @property
    def days_json(self):
        """
        Custom property to return days as json list instead of default python list.
        """
        return json.dumps(self['days'])


class OpenHoursBlock(blocks.StructBlock):
    """
    Holds day and time combination for business open hours.
    """
    days = MultiSelectBlock(
        required=True,
        verbose_name=_('Days'),
        help_text=_('For late night hours past 23:59, define each day in a separate block.'),
        widget=forms.CheckboxSelectMultiple,
        choices=(
            ('Monday', _('Monday')),
            ('Tuesday', _('Tuesday')),
            ('Wednesday', _('Wednesday')),
            ('Thursday', _('Thursday')),
            ('Friday', _('Friday')),
            ('Saturday', _('Saturday')),
            ('Sunday', _('Sunday')),
        ))
    start_time = blocks.TimeBlock(verbose_name=_('Opening time'))
    end_time = blocks.TimeBlock(verbose_name=_('Closing time'))

    class Meta:
        template = 'coderedcms/blocks/struct_data_hours.json'
        label = _('Open Hours')
        value_class = OpenHoursValue


class StructuredDataActionBlock(blocks.StructBlock):
    """
    Action object from schema.org
    """
    action_type = blocks.ChoiceBlock(
        verbose_name=_('Action Type'),
        required=True,
        choices=schema.SCHEMA_ACTION_CHOICES
    )
    target = blocks.URLBlock(verbose_name=_('Target URL'))
    language = blocks.CharBlock(
        verbose_name=_('Language'),
        help_text=_(
            'If the action is offered in multiple languages, create separate actions for each language.'),  # noqa
        default='en-US'
    )
    result_type = blocks.ChoiceBlock(
        required=False,
        verbose_name=_('Result Type'),
        help_text=_('Leave blank for OrderAction'),
        choices=schema.SCHEMA_RESULT_CHOICES
    )
    result_name = blocks.CharBlock(
        required=False,
        verbose_name=_('Result Name'),
        help_text=_('Example: "Reserve a table", "Book an appointment", etc.')
    )
    extra_json = blocks.RawHTMLBlock(
        required=False,
        verbose_name=_('Additional action markup'),
        form_classname='monospace',
        help_text=_(
            "Additional JSON-LD inserted into the Action dictionary. Must be properties of https://schema.org/Action."  # noqa
        )
    )

    class Meta:
        template = 'coderedcms/blocks/struct_data_action.json'
        label = _('Action')
