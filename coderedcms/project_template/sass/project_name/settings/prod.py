from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "{{ secret_key }}"

# Add your site's domain name(s) here.
ALLOWED_HOSTS = ["{{ domain }}"]

# To send email from the server, we recommend django_sendmail_backend
# Or specify your own email backend such as an SMTP server.
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#email-backend
# EMAIL_BACKEND = "django_sendmail_backend.backends.EmailBackend"

# Default email address used to send messages from the website.
DEFAULT_FROM_EMAIL = "{{ sitename }} <info@{{ domain_nowww }}>"

# A list of people who get error notifications.
ADMINS = [
    ("Administrator", "admin@{{ domain_nowww }}"),
]

# A list in the same format as ADMINS that specifies who should get broken link
# (404) notifications when BrokenLinkEmailsMiddleware is enabled.
MANAGERS = ADMINS

# Email address used to send error messages to ADMINS.
SERVER_EMAIL = DEFAULT_FROM_EMAIL

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "cache"),  # noqa
        "KEY_PREFIX": "coderedcms",
        "TIMEOUT": 14400,  # in seconds
    }
}
