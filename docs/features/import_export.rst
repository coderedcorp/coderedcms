Import/Export
=============

``wagtail-import-export`` is included in the CMS. You can find documentation for it
`here <https://github.com/torchbox/wagtail-import-export>`_.  In addition to the JSON
import/export functionality that the package includes, we have added the ability to create
pages by importing CSV files.

In the CSV each row will be a new page and each column header will correspond to an attribute
of that page. On the import CSV page, you will select where you want the pages to live and what
page type they should be created as. A use case for this functionality would be if your site needs
to add several hundred locations as pages. These locations come from a CSV dump from some report
generating software. Your CSV could look something like this::

    title       address         latitude    longitude
    Store 1     123 Street      20.909      -15.32
    Store 2     456 Avenue      34.223      87.2331
    ...
    ...

``title``, ``address``, ``latitude``, ``longitude`` are all fields on your Page model that you will
be importing as.

.. note::
    Your CSV file must be encoded as ASCII or UTF-8.
    UTF-8-BOM will cause an error.
