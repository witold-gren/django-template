"""
Test settings for {{cookiecutter.project_name}} project.

- Used to run tests fast on the continuous integration server and locally
"""

from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
# Turn debug off so tests run faster
DEBUG = False

# This needs to be enabled if we want to use the coverage plugin for templates
TEMPLATES[0]["OPTIONS"]["debug"] = {% if cookiecutter.use_django_rest_framework == 'y' %}False{% else %}True{% endif %}


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default="CHANGEME!!!")


# EMAIL
# ------------------------------------------------------------------------------
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# In-memory email backend stores messages in django.core.mail.outbox
# for unit testing purposes
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

{%- if cookiecutter.postgresql_version != 'No database' %}


# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST_NAME": ":memory:",
    }
}
{%- endif %}


# CACHING
# ------------------------------------------------------------------------------
# Speed advantages of in-memory caching without having to run Memcached
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}


# TESTING
# ------------------------------------------------------------------------------
# TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_RUNNER = "config.runner.PytestTestRunner"
{%- if cookiecutter.postgresql_version != 'No database' %}
AUTHENTICATION_BACKENDS += ["django_webtest.backends.WebtestUserBackend"]


MIDDLEWARE += ["django_webtest.middleware.WebtestUserMiddleware"]
{%- endif %}
{%- if cookiecutter.use_django_rest_framework == 'y' and cookiecutter.postgresql_version != 'No database' %}


REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (
    "config.webtest.WebtestAuthentication",
)
{%- endif %}
{%- if cookiecutter.use_celery == 'y' %}


# CELERY
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = True
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
{%- endif %}


# PASSWORD HASHING
# ------------------------------------------------------------------------------
# Use fast password hasher so tests run faster
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


# TEMPLATES
# ------------------------------------------------------------------------------
# Keep templates in memory so tests run faster.
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]["OPTIONS"]["loaders"] = [
    [
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    ]
]
