Add Tracking Scripts
====================

Tracking scripts, such as like Google Analytics or Facebook Pixels, can be added
to the ``<head>`` and ``<body>`` of all of your web pages.

Tracking settings are located in the Wagtail Admin dashboard under
**Settings > Tracking**.

.. warning::

   While it may be tempting to add dozens of tracking scripts to your website,
   keep in mind that **each script you add will slow your site down**
   and will invade your visitors' privacy. Therefore we recommend to carefully
   evaluate and choose one tracking solution that best fits your needs.


Google Analytics
----------------

There are two types of Google Analytics accounts --- "Universal Analytics"
(generally for accounts created before 2021) and "Google Analytics 4":

* **Universal Analytics** account IDs begin with **UA-**

* **Google Analytics 4 (GA4)** account IDs begin with **G-**

* If you are using both account types, you can enter both IDs and the data will
  populate both accounts. However, neither is "better" and using both does not
  provide any benefit compared to using just one.

.. note::

   A common misconception is that Google Analytics helps boost SEO. This is not
   true! Google Analytics tracks people who use your site so you can see
   metrics such as: how many people viewed which pages, for how long, from what
   location, etc. It does not provide any benefit other than giving you this
   information.


Google Tag Manager (GTM)
------------------------

Google Tag Manager (GTM) is a separate product from Google Analytics. GTM lets
you add **one** script to your site. Then, from the GTM Console, you can add
multiple other tracking scripts (Such as Google Analytics, Google Adwords,
Google Remarketing, Facebook Pixels, Salesforce, Pardot, StatCounter, Adobe,
etc.). GTM makes it convenient for your marketing staff to continually add and
change the tracking tools without having to make any changes to the website.

If you are using Google Tag Manager, we recommend that you remove any other
tracking scripts from your site, and add them instead through the GTM Console.


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

    You can verify that the scripts on the web page by going to the site and
    inspecting the Source Code. Then search for the ``<script>`` tags, either
    visually or by hitting ``CTRL + F`` on your keyboard and searching for the
    code. Here's how to get the Source Code if you are not sure:

    * Firefox: https://developer.mozilla.org/en-US/docs/Tools/View_source

    * Chrome: https://support.google.com/surveys/answer/6172725?hl=en

    * IE/Edge: https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide-chromium/resources/
