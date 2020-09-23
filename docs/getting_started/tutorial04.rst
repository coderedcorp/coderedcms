Tutorial Part 4: Creating a Blog
================================

We want to add a blog to our site, so let's get some practice with Article Pages!
Then we will get some practice building a basic web page as well.

Adding articles to the site
---------------------------

Okay, Articles will be child pages (also known as sub-pages) for the **Article Landing Page**. This
is important to remember because sub-pages can be accessed by the parent page (also known as the
landing page).

.. note::
    Before we can add any Articles, we have to create the Article Landing Page.

Click on **Pages > Home** to get to the screen that will allow you to create child pages under the Home page.
It looks like this:

.. figure:: img/tutorial_home_child_edit1.png
    :alt: Screen for adding pages under the Home page.

    The admin screen for adding pages under the Home page.

Click on the button that says **Add Child Page**. Because we are still using the built-in page types, you should
only see three types of pages available for now:

* **Article Landing Page** - The landing page for articles, blog posts, etc.

* **Form** - A page type for building forms.

* **Web Page** - A basic page type for building any type of web page.

.. figure:: img/tutorial_home_child_edit2.png
    :alt: Screen for Home page sub-page types.

    The admin screen for choosing sub-page types under the Home page.

Select the **Article Landing Page** to begin. For now, we will keep this particular page simple.
Just give it a title of Blog. Add a cover image if you would like one. Now **Publish** it. We will
come back to it later on in this tutorial.

Go back to the admin screen for adding pages under the Home page. You should now see the Article Landing
Page listed that we named Blog. Hover over it to reveal more options for Blog, and you should see the options
to add child pages to the Blog page. We want to add a few posts, so select **Add Child Page**. This will
take you to the Article page type for editing!

.. figure:: img/tutorial_blank_article.png
    :alt: A fresh article page in edit mode.

    The edit screen for a fresh article page.

The anatomy of an Article Page
------------------------------

The Article Page has several built-in fields to make it easy to publish an article, or blog as in our
case. We will want to fill in the following:

* **Title** - Title of the article or blog

* **Cover Image** - Not required but can add interest to your page

* **Caption** - The sub-title for the article or blog

* **Publication Info** - Here we add the author, the display name for the author if different, and the Publication date

* **Body** - Content for our article or blog

Let's write a short blog about the story of our cupcakes. Once we fill in the information we want to add above, we
can select what we want to add to the body of the blog post. We will choose a **Text** block.

After we add our Content in the Text block, we can add other types of content if we like. How about a button?
Select the + sign under the Text block, then choose **Button Link**. Continue to add different content blocks
as you see fit for the blog post.

.. figure:: img/tutorial_blog_post_edit.png
    :alt: The edit screen for our first blog post.

    The edit screen for our first blog post.

Now publish it and see what it looks like! This is what our blog post looks like:

.. figure:: img/tutorial_blog_post_published.png
    :alt: Our first published blog post.

    Our first published blog post.

Add a few more blog posts to get some practice, then we will return to our Blog landing page.

Completing our Blog landing page
--------------------------------

On the admin page, we can select to edit the main Blog page. Click the **Edit** button that is under the
word **Blog**. Alternatively, you can find the Blog page in the Home page admin view or by clicking on Pages.

.. figure:: img/tutorial_blog_admin_view.png
    :alt: Admin view to edit our pages.

    The admin view to edit our blog posts and our Blog landing page.

Just like on the other pages, we can add a cover image and build the layout. Let's do that! We will use
Responsive Grid Row and just one full-width column for an introduction. Then we will show you the different
ways to display your sub-pages on the landing page.

.. figure:: img/tutorial_blog_landing_edit1.png
    :alt: The edit screen showing our intro on Blog page

    The edit screen showing the introduction on our Blog landing page.

Publish and see what happens!

.. figure:: img/tutorial_blog_landing_published.png
    :alt: Our published Blog page

    The published Blog landing page.

Whoa! The blog posts are already showing up! What is this magic? Well, remember that this is a parent page type
and the blog posts were children of this page. The option to "show children" is already pre-selected in the edit mode
for the landing pages. We should go take a look at that now.

Ways to display sub-pages on a landing page
-------------------------------------------

Go back into the editor for the Blog landing page. You should see the following tabs at the top:

* **Content**

* **Classify**

* **Layout**

* **SEO**

* **Settings**

We want the **Layout** tab. Click on that tab and you'll see something like this:

.. figure:: img/tutorial_blog_landing_layout_tab.png
    :alt: The Layout tab for the Blog landing page

    The Layout tab for the Blog landing page.

We are using the default template, so skip over that for now. The sections titled
**"Show Child Pages"** and **"Child Page Display"** contain the settings for whether or not
the sub-pages (blogs in this case) are automatically pulled onto the page, how many
of them to show, and what fields or pieces of them to show as a preview.

.. note::
    The "Show Child Pages" setting in Layout is the simplest and easiest way to display
    your sub-pages on a landing page.

But we said that there are other ways to do this! Well, yes, there are. De-select "Show Child Pages"
in Layout so that we can try the other way of displaying your sub-pages. Then go back to the Content area.

You can add more content below the Text block with our introduction, or make a new column for content, or start
a new Responsive Grid Row to add a column with content.

What we want to look at is the **Latest Pages** block. The Latest Pages block is extra powerful because you can access
the sub-pages of **any landing page on the site**! You can look at it for now, but we are going to just use the "Show Child Pages"
in Layout after all. We will go into more depth about this block and other content blocks in the future.

Remember to re-select "Show Child Pages" in Layout before publishing it.
