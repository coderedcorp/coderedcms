import django.dispatch

def run_integrations(instance, **kwargs):

    for panel in instance.integration_panels:
        for integration in getattr(instance, panel.relation_name).all():
            integration.integration_signal_operation(instance, **kwargs)

form_page_submit = django.dispatch.Signal(providing_args=['instance',])
form_page_submit.connect(run_integrations)