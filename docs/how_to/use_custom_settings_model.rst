Using a Custom Settings Model
============================================

Wagtail CRX provides two settings models, `LayoutSettings` and
`AnalyticsSettings`, which enable admins to manage site-specific settings. If
you need to store additional site-specific settings and do not wish to have
multiple "Settings" menus, you can disable the default models and create a
custom settings model. 

There are abstract classes for each of the default settings models that you can
subclass or you can start from scratch, using the Wagtail CRX settings models as
a guide. The abstract classes are ``coderedcms.models.AbstractLayoutSettings``
and ``coderedcms.models.AbstractAnalyticsSettings``.


.. versionadded:: 3.0.4

    Added support for custom settings models. You must be on Wagtail CRX version
    3.0.4 or higher in order to follow this guide.


Step 1: Disable the default settings model(s)
---------------------------------------------

Disable one or both of the default settings models by adding the following to
your settings file::

    CRX_ENABLE_LAYOUT_SETTINGS = False
    CRX_ENABLE_ANALYTICS_SETTINGS = False

Setting these to ``False`` will prevent the default settings model from being
registered with Wagtail Admin.

Step 2: Create a custom settings model
--------------------------------------

Create a custom settings model by subclassing the appropriate base class and
adding your own fields. Register the model with the `@register_setting`
decorator, choosing an icon to represent the model in the admin.

For example

.. code-block:: python

    from wagtail.contrib.settings.models import register_setting    
    from coderedcms.models import AbstractLayoutSettings

    @register_setting(icon="cr-desktop")
    class CustomLayoutSettings(AbstractLayoutSettings):
        custom_field = models.CharField(max_length=255, blank=True, null=True)

        class Meta:
            verbose_name = "Custom Layout Settings"
            verbose_name_plural = "Custom Layout Settings"

.. note::

    The default models are always created so you must choose a different name
    for your custom model. More on this in `Step 4: Override the default
    templates` below.

Step 3: Create custom navbar and footer
---------------------------------------

If you subclass ``coderedcms.models.AbstractLayoutSettings``, you should define
your own navbar and footer models so that they can be selected in your custom
settings. If you do not subclass the default abstract class or do not add a
navbar or footer attribute to your custom settings, you can skip this step.

.. code-block:: python

    class CustomNavbarOrderable(Orderable, models.Model):
        navbar_chooser = ParentalKey(
            CustomLayoutSettings,
            related_name="site_navbar",
            verbose_name=_("Site Navbars"),
        )
        navbar = models.ForeignKey(
            Navbar,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
        )

        panels = [FieldPanel("navbar")]

    class CustomFooterOrderable(Orderable, models.Model):
        footer_chooser = ParentalKey(
            CustomLayoutSettings,
            related_name="site_footer",
            verbose_name=_("Site Footers"),
        )
        footer = models.ForeignKey(
            Footer,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
        )

        panels = [FieldPanel("footer")]

Step 4: Override the default templates
--------------------------------------

Wagtail CRX templates reference the default models. You must override the
following templates to reference your custom model:

* coderedcms/templates/wagtailadmin/base.html
* coderedcms/templates/coderedcms/pages/base.html
* coderedcms/templates/coderedcms/snippets/footer.html
* coderedcms/templates/coderedcms/snippets/navbar.html
* coderedcms/templates/coderedcms/blocks/google_map.html
* coderedcms/templates/coderedcms/pages/search.html

For example, copy ``coderedcms/templates/coderedcms/snippets/footer.html`` from
Wagtail CRX to ``templates/coderedcms/snippets/footer.html`` in your project and
change the second line so that:

.. code-block:: Django
    :emphasize-lines: 2

    {% load wagtailcore_tags coderedcms_tags %}
    {% if settings.coderedcms.LayoutSettings.site_footer %}
    <footer>
      {% get_footers as footers %}
      {% for footer in footers %}
      <div {% if footer.custom_id %}id="{{footer.custom_id}}"{% endif %} {% if footer.custom_css_class %}class="{{footer.custom_css_class}}"{% endif %}>
          {% for item in footer.content %}
          {% include_block item with settings=settings %}
          {% endfor %}
      </div>
      {% endfor %}
    </footer>
    {% endif %}

becomes:

.. code-block:: Django
    :emphasize-lines: 2

    {% load wagtailcore_tags coderedcms_tags %}
    {% if settings.coderedcms.CustomLayoutSettings.site_footer %}
    <footer>
      {% get_footers as footers %}
      {% for footer in footers %}
      <div {% if footer.custom_id %}id="{{footer.custom_id}}"{% endif %} {% if footer.custom_css_class %}class="{{footer.custom_css_class}}"{% endif %}>
          {% for item in footer.content %}
          {% include_block item with settings=settings %}
          {% endfor %}
      </div>
      {% endfor %}
    </footer>
    {% endif %}