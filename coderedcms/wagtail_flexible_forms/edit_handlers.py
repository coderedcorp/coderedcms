from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import EditHandler


class FormSubmissionsPanel(EditHandler):
    template = "wagtailforms/edit_handlers/form_responses_panel.html"

    def bind_to(self, model=None, instance=None, request=None, form=None):
        new = super().bind_to(model=model)
        if self.heading is None:
            new.heading = _('{} submissions').format(model.get_verbose_name())
        return new

    def render(self):
        Submission = self.model.get_submission_class()
        submissions = Submission.objects.filter(page=self.instance)
        submission_count = submissions.count()

        if not submission_count:
            return ''

        return mark_safe(render_to_string(self.template, {
            'self': self,
            'submission_count': submission_count,
            'last_submit_time': (submissions.order_by('submit_time')
                                 .last().submit_time),
        }))
