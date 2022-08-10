Best Practices for Images
=========================


For Editors
-----------

**Logo** and **Favicon**: Upload your logo and favicon under **Settings >
Layout** using high resolution PNG (or WebP) files. Any size or resolution is
acceptable. Note that the Favicon will be cropped to a square (1:1) aspect
ratio.

**Cover Images**: Cover images added to Web Pages, Article Pages, Event Pages,
etc. will all be scaled to a **16:9 aspect ratio** with a maximum resolution of
**1600x900 pixels**. Generally these should be uploaded in JPG (or WebP) format.
Any resolution is fine, but common resolutions such as 1280x720, 1600x900, etc.
are most appropriate. Avoid uploading huge "raw" image files (e.g. images
greater than 1 MB in file size).

**Image Blocks**: Images added in the page body (via the Image or Image Link
blocks) will keep their original aspect ratio preserved, but will be scaled to a
maximum width or height of 1600 pixels. Any aspect ratio or image resolution is
acceptable.


For Developers
--------------

.. versionadded:: 1.0

   Images are served in WebP format.

As of version 1.0, all images are served in WebP format. WebP format provides
the benefit of significantly smaller file sizes and results in an overall faster
website with better SEO performance. All mainstream browsers released after 2020
include WebP support. The following browsers and/or operating systems *do not*
support WebP, but might still be in use:

* Internet Explorer
* Safari on macOS 10 or older
* iOS 13 or older
* Consult the `full list of WebP browser support <https://caniuse.com/webp>`_

If your website needs to support these systems, we recommend having Wagtail
substitute WebP for JPG with the following setting in your Django settings file:

.. code-block:: python

   WAGTAILIMAGES_FORMAT_CONVERSIONS = {
       "webp": "jpeg",
    }

If you would like to support both WebP and alternative fallback image formats,
you may need to override the default CRX templates to use the `picture element
as described in the Wagtail docs
<https://docs.wagtail.org/en/stable/advanced_topics/images/image_file_formats.html>`_.
