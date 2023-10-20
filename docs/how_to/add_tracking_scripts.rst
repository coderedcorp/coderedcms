Add Tracking Scripts
====================

Tracking scripts, such as Google Analytics or Facebook Pixels, can be added to
the ``<head>`` and ``<body>`` of all of your web pages.

Tracking settings are located in the Wagtail Admin dashboard under
**Settings > Tracking**.

.. warning::

   Keep in mind that **each script you add will slow your site down** and may
   affect your data privacy compliance such as GDPR. Therefore we recommend to
   carefully evaluate and choose one tracking solution that best fits your
   needs.


Google Analytics
----------------

There are two types of Google Analytics accounts --- "Google Analytics 4" (GA4)
and "Universal Analytics" (which is discontinued as of July 2023):

* **Google Analytics 4 (GA4)** account IDs begin with **G-**

* **Universal Analytics** account IDs begin with **UA-**. Google shut
  down UA accounts in July 2023, so these will no longer work.

.. deprecated:: 3.0

   Support for Universal Analytics was removed in CRX version 3.0.


Google Tag Manager (GTM)
------------------------

Google Tag Manager (GTM) lets you add **one** script to your site. Then, from
the `Google Tag Manager Console <https://tagmanager.google.com/>`_, you can add
multiple other tracking scripts (Such as Google Analytics, Adwords, Facebook
Pixels, HubSpot, Salesforce, Pardot, StatCounter, Adobe, etc.). GTM makes it
convenient for your marketing staff to continually add and change the tracking
tools without having to make any changes to the website.

.. important::

   If you are using Google Tag Manager, you should remove any other tracking
   scripts from your site (including the **G-** and **UA-** IDs above), and add
   them through the `Google Tag Manager Console
   <https://tagmanager.google.com/>`_ instead.


Other Scripts
-------------

If you have other tracking codes to add, follow these steps:

#. In the Wagtail admin, go to **Settings > Tracking**.

#. The tracking scripts will usually give you instructions of where to place
   them. So, make sure to verify the instructions that were given to you.

#. Copy and paste scripts that should be between the ``<head>`` tags in the box
   labeled for ``<head>`` scripts.

#. Copy and paste scripts that should be toward the closing ``<body>`` tag in
   the box labeled for ``<body>`` scripts.

#. Click **Save** and you're done!


.. figure:: img/head-body-scripts-widgets.png
    :alt: The TRACKING dashboard.

    The tracking dashboard.

.. note::

    You can verify that the scripts are on the web page by going to the site and
    inspecting the source sode. Then search for the ``<script>`` tags, either
    visually or by hitting ``CTRL + F`` on your keyboard and searching for the
    code. Here's how to view the source code if you are not sure:

    * Firefox: https://developer.mozilla.org/en-US/docs/Tools/View_source

    * Chrome: https://support.google.com/surveys/answer/6172725?hl=en

    * Edge: https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide-chromium/resources/
