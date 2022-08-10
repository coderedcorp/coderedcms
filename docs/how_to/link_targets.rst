Open External Links in New Tab
==============================

A common requirement by marketing teams is to force external links to open in
a new tab, rather than to navigate the current tab. Wagtail has strong opinions
against this practice, hence Wagtail does not provide the ability to set the
``target`` attribute of links in rich text fields. But, the reality of the
matter is that not everyone shares this opinion.

Wagtail CRX provides a setting that will use JavaScript to open all external
links, meaning any link not on the current domain, to open with
``target='_blank'``:

**Settings > CRX Settings > Open all external links in
new tab**
