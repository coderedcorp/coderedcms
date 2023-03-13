Modal Block
===========

Creates a popup box with a header, footer, and the ability to display the body as a block.
Click the "X" in the corner or background of page to close it.

Example: (Modal Open Button)
    .. figure:: images/modal_button.jpeg
        :alt: The webpage with an open modal button.

        The webpage with an open modal button.  Can be styled like any other button see Button Block.

(Modal Open)
    .. figure:: images/modal_open.jpeg
        :alt: The webpage with an open modal button.

        The webpage with an open modal button.  Can be styled like any other button see Button Block.

Field Reference
---------------

Fields and purposes:

* **Button Title** - The text to show on the button. You can insert simple HTML
  here as well, such as ``Learn <b>More</b>``.

* **Button Style** - The appearance of the button. This is a choice loaded from
  ``CRX_FRONTEND_BTN_STYLE_CHOICES`` Django setting and is inserted as a
  CSS class in the HTML.

* **Button Size** - The size of button. This is a choice loaded from
  ``CRX_FRONTEND_BTN_SIZE_CHOICES`` Django setting and is inserted as a CSS
  class in the HTML.

* **Modal Heading** - The heading, or title, that will display on the modal

* **Content** - Choose from other content blocks for the body of the modal.

* **Modal Footer** - Choose a Simple Text footer or a button link

Once it is published, website visitors can click the button to see the popup message.

.. figure:: images/modal_editor.jpeg
    :alt: modal editing block

    Modal editing block
