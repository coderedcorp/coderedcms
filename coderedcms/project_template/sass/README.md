# {{ sitename }} website

## Getting started

Make sure Python 3.4 or higher is installed on your system.
Open this directory in a command prompt, then:

1. Install the software, and the dev tooling:
    ```
    pip install -r requirements.txt -r requirements-dev.txt
    ```

2. Build the Sass:
    ```
    python manage.py sass website/static/website/src/custom.scss website/static/website/css/
    ```
    To build the Sass automatically whenever you change a file, add the `--watch` option and run it in a separate terminal. For more options, see [django-sass](https://github.com/coderedcorp/django-sass/).

3. Run the development server:
    ```
    python manage.py runserver
    ```

4. Go to http://localhost:8000/ in your browser, or http://localhost:8000/admin/ to log in and get to work!

## Documentation links

* To customize the content, design, and features of the site see [CodeRed CMS](https://docs.coderedcorp.com/cms/).
* For deeper customization of backend code see [Wagtail](http://docs.wagtail.io/) and [Django](https://docs.djangoproject.com/).
* For HTML template design see [Bootstrap](https://getbootstrap.com/).

---

Made with ♥ using [CodeRed CMS](https://www.coderedcorp.com/cms/)
