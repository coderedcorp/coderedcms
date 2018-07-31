# Documentation

[< Back to README](README.md)

Table of Contents:
* [Quick Start](#quick-start)
* [Customizing your website](#customizing-your-website)
* [Searching](#searching)
* [Hooks](#hooks)
* [Settings](#codered-cms-settings)
* [Developing coderedcms](#developing-and-testing-codered-cms)




## Quick start
1. Run `pip install coderedcms`

2. Run `coderedcms start mysite`

3. Run `python manage.py migrate` to create the core models.

4. Run `python manage.py createsuperuser` to create the initial admin user.

5. Run `python manage.py runserver` to launch the development server, and go to `http://localhost:8000` in your browser, or `http://localhost:8000/admin/` to log in with your admin account.



## Customizing your website
After following the quickstart, you are greeted by a barebones website. There are a few settings you will want to change to add your own branding.

### Site name
This is shown by default in the navbar, and also added to the title attribute of each page. This can be changed in Settings > Sites > localhost. Hostname and port only need to be changed when running in  production.

### Site settings
Under Settings > Sites in the Wagtail Admin, you will want to make sure this setting is up to date with the proper Hostname and Port. Failure to do so can cause the Preview button on pages to return a 500 error.

### Logo & icon
The logo that appears in the navbar, the wagtail admin, and your favicon can be set in Settings > Layout. Here you can also change navbar settings (based on Bootstrap CSS framework).

### Navigation bars
Navbars are top navigation elements that create a "main menu" experience. Navbars are managed as snippets. They render from top down based on the order they were created in.

### Footers
Similar to Navbars, footers are also managed as snippets and also render top down based on the order they were created in.

### Custom CSS
A django app called `website` has been created to hold your custom changes. In website/static/ there are custom.css and custom.js files that get loaded on every page by default. Adding anything to these files will automatically populate on the site and override any default styles. By default, Bootstrap 4 and jQuery are already included on the site.

### Custom templates
The templates directory inside the `website` app is empty by default. Any templates you put in here will override the default coderedcms templates if they follow the same name and diretory structure. This uses the standard Django template rendering engine. For example, to change the formatting of the article page, copy `coderedcms/templates/coderedcms/pages/article_page.html` to `website/templates/coderedcms/pages/article_page.html` and modify it.

### Custom models
The django app `website` has been created with default models based on pre-built abstract CodeRed CMS models. You can use these as-is, override existing fields and function, and add custom fields to these models. After making a change to any of these models, be sure to run `python manage.py makemigrations` and `python manage.py migrate` to apply the database changes.


## Searching
A search page is available by default at the `/search/` URL, which can be customized in the `urls.py` file in your project. To enable a search bar in the navigation bar, check Settings > Layout > Search box. Search results are paginated; to specify the number of results per page, edit the value in Settings > General > Search Settings.

### Search result formatting
Each search result is rendered using the template at `coderedcms/pages/search_result.html`. The template can be overriden per model with the `search_template` attribute.

### Search result filtering
To enable additional filtering by page type, add `search_filterable = True` to the page model. The `search_name` and `search_name_plural` fields are then used to display the labels for these filters (defaults to `verbose_name` and `verbose_name_plural` if not specified). For example, to enable search filtering by Blog or by Products in addition to All Results:
```
class BlogPage(CoderedArticlePage):
    search_filterable = True
    search_name = 'Blog Post'
    search_name_plural = 'Blog'

class Product(CoderedWebPage):
    search_filterable = True
    search_name = 'Product'
    search_name_plural = 'Products'
```
Would enable the following filter options on the search page: All Results, Blog, Products.

### Search fields
If using the Wagtail DatabaseSearch backend (default), only page Title and Search Description fields are searched upon. This is due to a limitation in the DatabaseSearch backend; other backends such as PostgreSQL and Elasticsearch will search on additional specific fields such as body, article captions, etc. To enable more specific searching while still using the database backend, the specific models can be flagged for inclusion in search by setting `search_db_include = True` on the page model. Note that this must be set on every type of page model you wish to include in search. When setting this flag, search is performed independently on each page type, and the results are combined. So you may want to also specify `search_db_boost` (int) to control the order in which the pages are searched. Pages with a higher `search_db_boost` are searched first, and results are shown higher in the list. For example:
```
class Article(CoderedArticlePage):
    search_db_include = True
    search_db_boost = 10
    ...

class WebPage(CoderedWebPage):
    search_db_include = True
    search_db_boost = 9
    ...

class FormPage(CoderedFormPage):
    ...
```
In this example, Article search results will be shown before WebPage results when using the DatabaseSearch backend. FormPage results will not be shown at all, due to the absence `search_db_include`. If no models have `search_db_include = True`, All CoderedPages will be searched by title and description. When using any search backend other than database, `search_db_*` variables are ignored.



## Hooks
Building on the concept of wagtail hooks, there are some additional hooks in CodeRed CMS

### `is_request_cacheable`
The callable passed into this hook should take a `request` argument, and return a `bool` indicating whether or not the response to this request should be cached (served from the cache if it is already cached). Not returning, or returning anything other than a bool will not affect the caching decision. For example:
```
from wagtail.core import hooks

@hooks.register('is_request_cacheable')
def nocache_in_query(request):
    # if the querystring contains a "nocache" key, return False to forcibly not cache.
    # otherwise, do not return to let the CMS decide how to cache.
    if 'nocache' in request.GET:
        return False
```



## CodeRed CMS Settings
Default settings are loaded from coderedcms/settings.py. Available settings for CodeRed CMS:

### CODERED_CACHE_PAGES
Boolean on whether or not to load the page caching machinery and enable cache settings in the wagtail admin.

### CODERED_CACHE_BACKEND
The name of the django cache backend to use for CodeRed CMS. Defaults to `'default'` which is required by Django when using the cache.

### CODERED_PROTECTED_MEDIA_ROOT
The directory where files from File Upload fields on Form Pages are saved. These files are served through django using `PROTECTED_MEDIA_URL` and require login to access. Defaults to `protected/` in your project directory.

### CODERED_PROTECTED_MEDIA_URL
The url for protected media files from form file uploads. Defaults to '/protected/'

### CODERED_PROTECTED_MEDIA_UPLOAD_WHITELIST
The allowed filetypes for media upload in the form of a list of file type extensions. Default is blank. For example, to only allow documents and images: `['.pdf', '.doc', '.docx', '.txt', '.rtf', '.jpg', '.jpeg', '.png', '.gif']`

### CODERED_PROTECTED_MEDIA_UPLOAD_BLACKLIST
The disallowed filetypes for media upload in the form of a list of file type extensions. Defaults to `['.sh', '.exe', '.bat', '.app', '.jar', '.py', '.php']`

### CODERED_FRONTEND_\*
Various frontend settings to specify defaults and choices used in the wagtail admin related to rendering blocks, pages, and templates. By default, all CODERED_FRONTEND_\* settings are designed to work with Bootstrap 4 CSS framework, but these can be customized if using a different CSS framework or theme variant.



## Developing and testing codered-cms
To create a test project locally before committing your changes:

1. Run `pip install -e ./` from the codered-cms directory. The -e flag makes the install editable, which is relevant when running makemigrations in test project to actually generate the migration files in the codered-cms pip package.

2. Follow steps 3 through 5 in the quickstart above. Use "testproject" or "testapp" for your project name to ensure it is ignored by git.

3. When making model or block changes whithin coderedcms, run `makemigrations coderedcms` in the test project to generate the relevant migration files for the pip package. ALWAYS follow steps 3 and 4 in the quickstart above with a fresh database before making migrations.

4. When model or block changes affect the local test project (i.e. the "website" app), run `makemigrations website` in the test project to generate the relevant migration files locally. Apply and test the migrations. When satisfied, copy the new migration files to the `project_template/website/migrations/` directory.

When making changes that are potentially destructive or backwards incompatible, increment the minor version number until coderedcms reaches a stable `1.0` release. Each production project that uses coderedcms should specify the appropriate version in its requirements.txt to prevent breakage.

### Building pip packages
To build a publicly consumable pip package, run:

    python setup.py sdist bdist_wheel

which will build a source distribution and a wheel in the `dist/` directory.
