FROM python:3.6-alpine

#
# Handle the env info
#
ARG BUILD_COMMIT_SHA1
ARG BUILD_COMMIT_DATE
ARG BUILD_BRANCH
ARG BUILD_DATE
ARG BUILD_REPO_ORIGIN
 
ENV BUILD_COMMIT_SHA1=$BUILD_COMMIT_SHA1
ENV BUILD_COMMIT_DATE=$BUILD_COMMIT_DATE
ENV BUILD_BRANCH=$BUILD_BRANCH
ENV BUILD_DATE=$BUILD_DATE
ENV BUILD_REPO_ORIGIN=$BUILD_REPO_ORIGIN

WORKDIR /src/
ADD . /src/

RUN apk update \
    && apk add build-base \
    jpeg-dev \
    zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

ENV PYTHONUNBUFFERED 1

RUN pip install pip
RUN python setup.py install

# uWSGI will listen on this port
EXPOSE 8000

# # Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
# RUN DATABASE_URL=none /venv/bin/python manage.py collectstatic --noinput

# Start uWSGI
ENTRYPOINT ["coderedcms"]
#CMD ["/venv/bin/uwsgi", "--http-auto-chunked", "--http-keepalive"]