Classifiers
===========

Classifiers provide a way to create custom categories or groups to organize and filter pages.


Usage
-----

Let's say you want to create a custom category: "Blog Category". Blog Category will be used
to filter article/blog pages on the site.

First, create a new Classifier under **Snippets > Classifiers** called "Blog Category"
and add several Terms underneath the Classifier, for example: "News", "Opinion", and "Press Releases".
These terms will function as categories. Create and reorder these Terms as needed.
Save the Classifier when finished.

Second, classify various Article pages by Blog Category terms:

* Edit an Article page.
* Open the **Classify** tab, and select the appropriate terms.
* Publish the page when finished.

To enable filtering Article pages by "Blog Category":

* Edit your Article Landing Page (may be named differently on your project - it should be the
  parent page of your Article Pages).
* Open the **Layout** tab, enable **Show child pages**, and then select "Blog Category"
  under **Filter child pages by** .
* Publish or preview the page, and you'll now see filtering options for every term under
  Blog Category.

Going a bit further, let's show a preview of the top 3 newest blog pages classified as "News"
automatically on the home page:

* Edit the home page.
* In the **Content** tab anywhere in the **Body** add a Responsive Grid Row, and then add a
  **Latest Pages** block.
* Set the **Parent page** to your Article landing page, and **Classified as** to
  "Blog Category > News".
* Publish or preview the page, and you'll now see the latest 3 articles classified as "News"
  on the home page.

Classifiers are not just limited to Article pages, they work an every page on the site.
Classifiers can be used to create product types, portfolios, categories, and any other
organizational structures your content may need.


Implementation
--------------

Classifiers are enabled by default on all ``CoderedPage`` models. The filtering HTML UI
is rendered in the ``{% block index_filters %}`` block on the page template, which originates
in ``base.html`` but is overridden in various other templates such as ``web_page_notitle.html``
and ``article_index_page.html``.

CodeRed CMS provides two filtering templates by default, a Bootstrap nav in
``coderedcms/includes/classifier_nav.html`` and a simple select/dropdown form in
``coderedcms/includes/classifier_dropdowns.html``. Most likely, you will want to implement your
own filtering UI based on your own website needs, but you can follow the example in these two
templates.

Classifiers are not limited to just Pages though - they can be used on Snippets or any other
model (Snippet example below)::

    from django.db import models
    from modelcluster.fields import ParentalManyToManyField
    from wagtail.admin.edit_handlers import FieldPanel
    from wagtail.snippets.models import register_snippet

    @register_snippet
    class MySnippet(models.Model):
        name = models.CharField(
            max_length=255,
        )
        classifier_terms = ParentalManyToManyField(
            'coderedcms.ClassifierTerm',
            blank=True,
        )
        panels = [
            FieldPanel('name')
            FieldPanel('classifier_terms'),
        ]


This will create a default list of checkboxes or a multi-select in the Wagtail UI
to select classifier terms. However, if you prefer to have the checkboxes grouped
by the Classifier they belong to (same UI as the **Classify** tab in the page editor),
use the built-in ``ClassifierSelectWidget``::

        from coderedcms.widgets import ClassifierSelectWidget

        panels = [
            FieldPanel('name')
            FieldPanel('classifier_terms', widget=ClassifierSelectWidget()),
        ]


Finally run ``python manage.py makemigrations website`` and ``python manage.py migrate`` to
create the new models in your project.
