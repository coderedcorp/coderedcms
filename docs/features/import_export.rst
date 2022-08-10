Import Pages
============

CRX includes the ability to import pages from CSV files. This is useful for
example in a store locator, where a list of stores needs to be uploaded
periodically.

To start an import, go to **Settings > Import**

In the CSV each row will be a new page and each column header will correspond to an attribute
of that page. On the import CSV page, you will select where you want the pages to live and what
page type they should be created as. A use case for this functionality would be if your site needs
to add several hundred locations as pages. These locations come from a CSV dump from some report
generating software. Your CSV could look something like this:

.. code-block:: text

    title   ,   address    ,   latitude ,   longitude
    Store 1 ,   123 Street ,   20.909   ,   -15.32
    Store 2 ,   456 Avenue ,   34.223   ,   87.2331
    ...
    ...

``title``, ``address``, ``latitude``, ``longitude`` are all fields on your Page model that you will
be importing as.

.. important::

    Your CSV file must be encoded as ASCII or UTF-8.
    UTF-8-BOM will cause an error.

.. versionchanged:: 0.24

   In version 0.24, the ability to import/export pages from JSON was removed.
   The Import/Export link in the side menu was also moved to Settings > Import.
