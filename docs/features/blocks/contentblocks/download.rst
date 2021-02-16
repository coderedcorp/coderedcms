Download Block
==============

The download block enables users to add documents to the CMS which website 
visitors can download from the site.

Field Reference
---------------

* **Button Title** - The text to show on the button. You can insert simple HTML
  here as well, such as ``Learn <b>More</b>``.

* **Button Style** - The appearance of the button. This is a choice loaded from
  ``CODERED_FRONTEND_BTN_STYLE_CHOICES`` Django setting and is inserted as a
  CSS class in the HTML.

* **Button Size** - The size of button. This is a choice loaded from
  ``CODERED_FRONTEND_BTN_SIZE_CHOICES`` Django setting and is inserted as a CSS
  class in the HTML.

* **Auto Download** - Enables automatic download upon click of the button

* **Document Link** - Link to the document, which you will need to upload into the CMS

* **Advanced Settings** - Add custom CSS classes or a CSS ID to style the block with your custom CSS 

.. figure:: img/blocks_download.png
    :alt: A download block and its settings.

    A download block and its settings.

.. figure:: img/blocks_choose_doc.png
    :alt: Choosing the document 

    The popup for choosing which document you want to upload to the block for download by users

When a website visitor clicks the button, the document is available for download in a new window. 