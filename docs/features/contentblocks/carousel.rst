Carousel Block
==============

Allows the user to create a carousel with image backgrounds and relevant blocks.
Carousel automatically change slides, but also have arrow controls for the user to advance or return to the previous slide.
Make a Carousel by going to **Snippets > Carousels** and clicking Add Carousel.

Field Reference
---------------

Fields and purposes:

* **Carousel** - Choose a Carousel

If you don't have any carousels already made, you can build a carousel by clicking **Choose A Carousel** and
clicking on "Why not **create one now**?" in the popup box. This will take you to **Snippets > Carousels** where
you can create a carousel to add to the page.

.. figure:: images/carousel_editor.jpeg
    :alt: Building a carousel in Snippets

    The edit mode for building a carousel snippet

Now you can select your carousel. Ours is named Demo.  Here is a preview of for one of our slides:

.. figure:: images/carousel_preview.jpeg
    :alt: Our carousel published on the page

    The carousel published on a page

It's hard to see the caption.  The bootstrap default is white text.
One answer would be to chose images that work well with white text.
That might not be ideally for you application.  Here are a few solutions.

Override the CSS class.  If you look at the `bootstrap docs <https://getbootstrap.com/docs/5.2/components/carousel/>`_ or the template.
You'll find the class for caption is ``carousel-caption``.  For our example, let's add a background color and border-radius.

.. code:: CSS

        .carousel-caption{
            background-color: rgba(60, 6
            0, 60, 0.5);
            border-radius: 10px;
        }

Add this to your custom.css file (basic installation) or the custom.scss file (sass installation).
Save the file, compile the sass(sass install only), and hard refresh the browser.  See :ref:`adding_custom_css`

.. figure:: images/carousel_preview_bg.jpeg
    :alt: Our carousel published on the page

    The carousel published on a page

Another option would be to alter the template.
Looking at the `bootstrap docs <https://getbootstrap.com/docs/5.2/components/carousel/>`_ you can find there is a dark variant.
See :ref:`customizing_templates` for a more detailed tutorial.

* To alter our template you need to copy the template from `github <https://github.com/coderedcorp/coderedcms/blob/dev/coderedcms/templates/coderedcms/blocks/carousel_block.html>`_
* Paste the file in the correct directory so it overrides the default template. Our file path: **mysite>website>templates>coderedcms>blocks>carousel_block.html**
* In carousel_block.html on line 4; add carousel-dark to the class attribute.  The line should now look like this:

.. code:: html

    <div id="carousel-{{self.carousel.id}}" class="carousel carousel-dark slide" data-bs-ride="carousel">

* Save the file and refresh the browser.

(In this example, I removed the custom css for .carousel-caption from the previous example)

.. figure:: images/carousel_preview_dark.jpeg
    :alt: Our carousel published on the page

    The carousel published on a page

