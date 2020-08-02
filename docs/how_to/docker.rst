Run CodeRed CMS with Docker
===========================

CodeRed CMS runs well in Docker. When working with Docker, there are two
different approaches. This guide will also work with any Wagtail site, or most
types of Django sites.

The first step is to `install Docker`_, on both your development environment
(i.e. your computer) and on your server (hosting) environment.

For the sake of this guide, we will assume your Django project is named
``myproject``.

.. _install Docker: https://docs.Docker.com/engine/install/



Step 1: Choose How to Use Docker
--------------------------------

The Versioned Image Approach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most common way of working with Docker is to create a static Docker image,
containing all of your code, which is effectively versioned in tandem with your
git repository. Each time you change your project code, you also create a new
version of the image. Because this image is effectively static and mirrors

version control, there is no way to store dynamic files such as a database or
media files. In this setup, you would want to use 3rd party services such as AWS
S3 for files, or AWS RDS for database. Nearly all cloud platforms provide
similar services.

Next, create a file in your main project folder named ``Dockerfile`` (no file
extension). Copy the contents below into the file:

.. code-block:: dockerfile

    FROM python:latest

    ENV PYTHONUNBUFFERED 1

    # Set the Django settings to use.
    ENV DJANGO_ENV "dev"
    ENV DJANGO_SETTINGS_MODULE "myproject.settings.dev"

    # Install a WSGI server into the container image.
    RUN pip install waitress

    # Code will end up living in /app/
    WORKDIR /app/

    # Copy and install the project requirements.
    COPY ./requirements.txt /app/requirements.txt
    RUN pip install -r /app/requirements.txt

    # Copy the entire project code.
    COPY . /app/

    # Prepare the app.
    RUN python manage.py migrate
    RUN python manage.py collectstatic --noinput

    # Create a "coderedcms" user account to run the app.
    RUN useradd coderedcms
    RUN chown -R coderedcms /app/
    USER coderedcms

    # Finally, run the app on port 8000.
    EXPOSE 8000
    CMD exec waitress serve --listen "*:8000" "myproject.wsgi:application"


The "Image as Environment" Approach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second approach is to use the container as the runtime environment, but
store your code and files outside the container. This way you only need to
update the container when you want to change your python version, or apply other
security updates. For those who like to use the filesystem, such as writing
logs, media files, etc. "normally", this is the recommended way to use Docker, as
it will fit within your existing workflow.

First, create a script which will be used as the entry point, meaning it runs
every time the container starts. The entry point will be used to set up the app
each time. Copy the contents below into a filed named ``docker-entrypoint.sh``.

.. code-block:: shell

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py collectstatic --noinput

Next, create a file in your main project folder named ``Dockerfile`` (no file
extension). Copy the contents below into the file:

.. code-block:: Dockerfile

    FROM python:latest

    ENV PYTHONUNBUFFERED 1

    # Set the Django settings to use.
    ENV DJANGO_ENV "dev"
    ENV DJANGO_SETTINGS_MODULE "myproject.settings.dev"

    # Install a WSGI server into the container image.
    RUN pip install waitress

    # Code will end up living in /app/
    WORKDIR /app/

    # Create a "coderedcms" user account to run the appp.
    RUN useradd coderedcms
    RUN chown -R coderedcms /app/
    USER coderedcms

    # Copy our entrypoint script.
    COPY ./docker-entrypoint.sh /usr/local/bin/
    RUN chmod +x /usr/local/bin/docker-entrypoint.sh

    # Finally, run the app on port 8000.
    EXPOSE 8000
    ENTRYPOINT ["docker-entrypoint.sh"]
    CMD exec waitress serve --listen "*:8000" "myproject.wsgi:application"


Step 2: Build and Run Your Image
--------------------------------


Next, with Docker running on your machine, create an image by running the
following from your command line, replacing ``/path/to/Dockerfile`` and
``/path/to/project/`` with the correct paths on your machine.

.. code-block:: console

    $ docker build --pull -t myproject:v1 -f /path/to/Dockerfile /path/to/project/

This will likely take a while, as Docker is going to download the ``FROM`` image
(Python in this case) and then run all of those commands in your Dockerfile.
Once complete, this will have created an image named ``myproject`` tagged with
``v1``. If you are using the "Versioned Image" approach, you would likely want
to change this tag every time you build the image. Docker image tags work
essentially like version control, as such many people choose to use their
current git commit ID as the tag. If you are using the "Image as Environment"
approach, then this tag would likely be your Python version, e.g. ``py3.8.1``

Now, create a container using the image. If using the "Versioned Image"
approach:

.. code-block:: console

    $ docker run --publish 8000:8000 --detach --name myproject-run myproject:v1

If using the "Image as Environment" approach, you also need to map a local
directory on your machine to a directory inside the container. This ensures that
the files that get created or modified are shared between your machine and the
container, and they will remain on your machine after the container is deleted.
The command below runs the container, but before doing so mounts the local directory
``./`` into the container's ``/app/`` directory:

.. code-block:: console

    $ docker run --publish 8000:8000 --detach --name myproject-run --mount type=bind,source=./,target=/app myproject:v1

Either approach will run an instance of your image ``myproject:v1`` named
``myproject-run``, and map port 8000 on your machine to port 8000 of the
container. Now going to http://localhost:8000 should serve up your app from the
container.

Read the official Docker guide and documentation at:
https://docs.docker.com/get-started/.
