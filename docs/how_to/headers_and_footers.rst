Create header and footer overrides
==================================

You are new to CodeRedCMS/Wagtail, but you want to get up and running quickly...

It isn't immediately obvious how to edit the header and a footer hasn't been created yet.

A header snippet is created and inserted for you by CodeRedCMS automatically, which is a nice thing that a vanilla Wagtail installation does not have.

Customizing the stock navbar can be accomplished by baked in conventional override.

You will need to add a file into the **templates\coderedcms\snippets** directory. You will likely need to create the aforementioned snippets directory.

Into that directory you will create a file called "navbar.html" . This file will be used instead of the navbar.html file of the CodeRedCMS pip package.

It is advisable to initially use the contents of `CodeRedCMS - Master Branch - navbar.html <https://github.com/coderedcorp/coderedcms/blob/master/coderedcms/templates/coderedcms/snippets/navbar.html>`_ .
...Advisable, but not necessary.

For the footer, you can add a footer snippet via the built in GUI admin interface under **Snippets > Footer**
