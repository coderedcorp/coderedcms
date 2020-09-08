Advanced: Customizing HTML/CSS in Templates
===========================================

Overview
---------
CodeRed CMS is an extension of Wagtail CMS. You can further customize your site by overriding the 
built-in templates to suit your needs. For this tutorial, we will assume that you have basic knowledge 
of the Django templating language. You can read more about it by visiting
`Django template language <https://docs.djangoproject.com/en/3.0/ref/templates/language/>`_.

The templating language uses a series of ``{%  %}`` to pull in content from your page models (found in 
the models.py file) and add minimal logic to the page. This allows it to render the page after content 
is added in the CMS and allows you to create multiple pages with the same layout. At the top of the page,
you also want to make sure to either specify that you are **extending a page template** and that you are 
pulling in Wagtail tags to make your template work the way it should. 

.. note::
    If you are completely overriding a template, you will not use the ``{% extends "path/to/template" %}`` 
    at the top of your template. You do, however, need to make sure to use the appropriate Wagtail 
    tags at the top of the template or your template will not render.

Example 1: Navbar Customization
-------------------------------

The built-in template for the navbar can be found in ``templates/coderedcms/snippets/navbar.html``. This 
file may not actually be in your installation folders for your site; however, you can see its contents 
by visiting the GitHub page for the code here: `Snippets – Navbar <https://github.com/coderedcorp/coderedcms/blob/dev/coderedcms/templates/coderedcms/snippets/navbar.html>`_. 

Let’s say that you want to have a 2-tiered navbar with the logo on the top tier and the menu items on the
second tier. The default navbar does not have that as an option, so you will want to override this template. 

Look at your folder structure for your project. In the ``website`` folder, you should see another folder 
called ``templates``. In there are two folders as well: ``website`` and ``coderedcms``. The ``coderedcms`` template 
folder is likely empty at this point because the CMS is pulling in the default templates from source, but you can 
add templates to the ``coderedcms`` folder **if you are overriding the default templates**.

Most of your custom templates will go into your ``website`` folder because they are not overriding the 
default templates in the CMS but either extending them or creating completely new ones specific to 
your site. 

.. note::
    Adding templates to the ``coderedcms`` templates folder does not change the default templates 
    throughout all of CodeRed CMS but does override those specific templates for your website app.

Your ``website`` folder currently only has a folder for ``coderedcms`` in the ``templates`` folder. 
You can add a new ``website`` folder in ``templates`` (because we will use it in another tutorial), 
but for now, you will want to add a ``snippets`` folder inside the ``templates\coderedcms`` folder 
so that your folder structure looks something like this:

.. figure:: img/advanced_folder_structure1.png
    :alt: Our folder structure for templates.

    Our folder structure for templates within our website app.

The folder structure needs to be the same as the default folder structure in the CMS if you want to 
override the navbar template. Now you should have ``templates\coderedcms\snippets``. Navigate to 
the ``snippets`` folder and create a ``navbar.html`` file inside of that folder. 

**You are now ready to begin customizing the navbar template!**

1.	Examine the default template for the navbar. What code will we want to use from it? You can use 
what’s there in your customization.

2. We will need the Wagtail tags at the top, so copy those and paste them into 
your ``navbar.html`` file.

.. code-block:: Django

    {% load wagtailcore_tags wagtailsettings_tags wagtailimages_tags coderedcms_tags i18n %}

3.	Next, we need to figure out how to move the logo (aka the ``navbar-brand``) into its own section for
the navbar. Maybe we could essentially create two navbars, one that just has the logo and one that has 
the menu. Hmm, let’s try that!

4.	We want to preserve the basic functionality of the navbar, so we should keep the tags for CMS settings 
and the overall layout inside of a container. 

5.	The 2-tiered navbar will have two navbars on top of each other but one will only have the
``navbar-brand`` (logo) while the other will allow for adding menu items via the CMS. So, the top 
navbar is not going to have access to CSS settings in the CMS that are reserved for the main navbar –- 
which means that you will need to add any custom classes to the top navbar, such as the background 
color or where you want the logo to be placed. Keep that in mind.

.. code-block:: Django

    {% load wagtailcore_tags wagtailsettings_tags wagtailimages_tags coderedcms_tags i18n %}


    {% if not settings.coderedcms.LayoutSettings.navbar_wrapper_fluid %}
    <div class="container">
    {% endif %}
    <nav class="navbar navbar-header bg-warning">
    
    {% if not settings.coderedcms.LayoutSettings.navbar_content_fluid %}
    <div class="container">
    {% endif %}
        <div class="logo-banner">
        <a class="navbar-brand" href="/">
            {% if settings.coderedcms.LayoutSettings.logo %}
            {% image settings.coderedcms.LayoutSettings.logo original as logo %}
            <img class="img-fluid" src="{{logo.url}}" alt="{{site.site_name}}" />
            {% else %}
            {{site.site_name}}
            {% endif %}
        </a>
        </div>
    {% if not settings.coderedcms.LayoutSettings.navbar_content_fluid %}
    </div><!-- /.container -->
    {% endif %}

    </nav>

We have set the foundation for the top navbar, which will be the banner section for the logo. Instead of
``<nav class="navbar {% get_navbar_css %}">``, we have added our own Bootstrap classes since this part of the
navbar will not be getting its CSS settings from the CMS.

However, we did keep the ``{% if settings.coderedcms.LayoutSettings.logo %} {% endif %}`` block because we want
to show the name of the site **if no logo is uploaded in the CMS**.  

6. Now we can include the code block for the normal navbar beneath it. Place this code below the ``</nav>`` in
your template. We want to preserve majority of the navbar as-is (without the block for ``navbar-brand``) so that
when we add menu items in the CMS, those items will show up as navigation links.

.. code-block:: Django

    <!--Put this below the previous nav closing tag -->

    <nav class="navbar {% get_navbar_css %}">

    {% if not settings.coderedcms.LayoutSettings.navbar_content_fluid %}
    <div class="container">
    {% endif %}
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbar">
        {% get_navbars as navbars %}
        {% for navbar in navbars %}
        <ul class="navbar-nav {{navbar.custom_css_class}}"
            {% if navbar.custom_id %}id="{{navbar.custom_id}}"{% endif %} >
            {% for item in navbar.menu_items %}
                {% include_block item with liclass="nav-item" aclass="nav-link" ga_event_category="Navbar" %}
            {% endfor %}
        </ul>
        {% endfor %}
        {% if settings.coderedcms.LayoutSettings.navbar_search %}
        <form class="ml-auto form-inline" action="{% url 'codered_search' %}" method="GET">
            {% load bootstrap4 %}
            {% get_searchform request as form %}
            {% bootstrap_form form layout='inline' %}
            <div class="form-group">
                <button class="btn btn-outline-primary ml-2" type="submit">{% trans 'Search' %}</button>
            </div>
        </form>
        {% endif %}

        </div>

    {% if not settings.coderedcms.LayoutSettings.navbar_content_fluid %}
    </div><!-- /.container -->
    {% endif %}

    </nav>

    {% if not settings.coderedcms.LayoutSettings.navbar_wrapper_fluid %}
    </div><!-- /.container -->
    {% endif %}

    {# Navbar offset #}
    {% if settings.coderedcms.LayoutSettings.navbar_fixed %}
        {% if settings.coderedcms.LayoutSettings.logo %}
        <div class="{{settings.coderedcms.LayoutSettings.navbar_format}}-fixed-img-offset {{settings.coderedcms.LayoutSettings.navbar_collapse_mode}}"></div>
        {% else %}
        <div class="{{settings.coderedcms.LayoutSettings.navbar_format}}-fixed-offset {{settings.coderedcms.LayoutSettings.navbar_collapse_mode}}"></div>
        {% endif %}
    {% endif %}

Let's talk about what is happening here. So, we pulled in the code for the navbar a second time, with the removal of
``navbar-brand`` section from the original template, but preserved majority of the default code for this section.
The ``if`` statements refer to whether or not some settings are chosen in the CMS and tells the template what to do in those
cases. We also needed to close to top-level ``container``. 

Another section that we kept was for the ``navbar-toggler``, which sets the hamburger menu when the screen sizes change. 
Finally, we also kept the ``{% get_navbar_css %}`` tag in the class for the ``nav`` because we can use CSS classes for this
navbar from the CMS. 

.. note::
    To add classes in the CMS, look for the line **Custom CSS Class**, which can be found as a field in sections of
    the admin for a snippet or page, or in the **Advanced** section of a Layout Block. This is where you would put a class
    like ``bg-warning`` from Bootstrap or a class that you created yourself, like ``logo-banner``. 

**Now for custom CSS**

If you noticed, we have a few custom classes that are not found in Bootstrap. To style our navbar with these classes,
we need to include them in our CSS file and set the styles the way we want. Once you've done that and saved your work,
your navbar is ready to show the world!
