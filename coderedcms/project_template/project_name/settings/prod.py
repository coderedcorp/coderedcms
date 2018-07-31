from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ secret_key }}'

# Add your site's domain name(s) here.
ALLOWED_HOSTS = []

# To send email from the server, we recommend django_sendmail_backend
# Or specify your own email backend such as an SMTP server.
EMAIL_BACKEND = 'django_sendmail_backend.backends.EmailBackend'

# A list of people who get error notifications.
ADMINS = [('Admin Name', 'admin@localhost')]

# A list in the same format as ADMINS that specifies who should get broken link
# notifications when BrokenLinkEmailsMiddleware is enabled.
MANAGERS = ADMINS

# Email address used to send error messages to ADMINS.
SERVER_EMAIL = '{{ project_name }}@localhost'

# Default email address used to send messages from the website.
DEFAULT_FROM_EMAIL = '{{ project_name}}@localhost'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'HOST': 'localhost',
#        'NAME': '{{ project_name }}',
#        'USER': '{{ project_name }}',
#        'PASSWORD': '',
#    }
#}

# Use template caching to speed up wagtail admin and front-end.
# Requires reloading web server to pick up template changes.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
        'KEY_PREFIX': 'coderedcms',
        'TIMEOUT': 3600, # in seconds
    }
}

try:
    from .local import *
except ImportError:
    pass
