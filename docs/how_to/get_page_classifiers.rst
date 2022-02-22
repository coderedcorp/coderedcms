Get Classifier Terms for Pages in a Template
============================================

You can include your classifier terms for your pages in your template with code similar
to the below:

.. code-block:: Django

    {% for term in page.classifier_terms.all %}
    <span>{{ term.name }}</span>
    {% endfor %}


If you only want to show specific terms, you can do something like this:

.. code-block:: Django

    {% for term in page.classifier_terms.all %}
    {% if term.slug=="the-term-slug" %}
    <span>{{ term.name }}</span>
    {% endif %}
    {% endfor %}

