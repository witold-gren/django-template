"""
Base settings for {{cookiecutter.project_name}} project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import pathlib

import environs

# ./{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}
APPS_DIR = pathlib.Path(__file__).parents[2]

# Load operating system environment variables and then prepare to use them
env = environs.Env()

# APP
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    {%- if cookiecutter.postgresql_version != 'No database' %}
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    {%- else %}
    "django.contrib.sessions",
    {%- endif %}
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    {%- if cookiecutter.postgresql_version != 'No database' %}
    "django.contrib.admin",
    {%- endif %}
]

THIRD_PARTY_APPS = [
    "health_check",
    {%- if cookiecutter.postgresql_version != 'No database' %}
    "health_check.db",
    {%- endif %}
    "health_check.cache",
    "health_check.contrib.psutil",
    #"health_check.contrib.celery",  # create simple task in all queues and wait 3sec
    #'health_check.storage',  # save and delete file in storage
    #'health_check.contrib.s3boto_storage',  # requires boto and S3BotoStorage backend
    #'health_check.contrib.rabbitmq',  # requires RabbitMQ broker
    {%- if cookiecutter.use_django_rest_framework == 'n' or cookiecutter.use_django_allauth == 'y' %}
    "crispy_forms",  # form layouts
    {%- endif %}
    {%- if cookiecutter.use_django_allauth == 'y' and cookiecutter.postgresql_version != 'No database' %}
    "allauth",  # registration
    "allauth.account",  # registration
    "allauth.socialaccount",
    {%- endif %}
    {%- if cookiecutter.use_django_rest_framework == 'y' %}
    "rest_framework",
    "rest_framework.authtoken",
    {%- if cookiecutter.postgresql_version != 'No database' %}
    "rest_auth",
    {%- endif %}
    {%- endif %}
    {%- if cookiecutter.use_django_channels == 'y' %}
    "channels",
    {%- endif %}
    "corsheaders",
    {%- if cookiecutter.use_graphql == 'y' %}
    "graphene_django",
    {%- endif %}
]

# Apps specific for this project go here.
LOCAL_APPS = [
    {%- if cookiecutter.postgresql_version != 'No database' %}
    # Custom users app
    "{{cookiecutter.project_slug}}.users.apps.UsersConfig",
    {%- endif %}
    # Your stuff: custom apps go here
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARES
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    {%- if cookiecutter.postgresql_version != 'No database' %}
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    {%- endif %}
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
{%- if cookiecutter.postgresql_version != 'No database' %}


# MIGRATIONS
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {"sites": "{{cookiecutter.project_slug}}.contrib.sites.migrations"}
{%- endif %}


# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)


# FIXTURES
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (APPS_DIR / "shared" / "fixtures",)
{%- if cookiecutter.use_django_amazon_ses == 'n' %}


# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
{%- endif %}


# MANAGERS
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""{{cookiecutter.author_name}}""", "{{cookiecutter.email}}")]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# DATABASES
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept uri format
# See: https://django-environ.readthedocs.io/en/latest/#supported-types
{%- if cookiecutter.postgresql_version != 'No database' %}
DB_USER = env("POSTGRES_USER", default="")
DB_PASSWORD = env("POSTGRES_PASSWORD", default="")
DB_PORT = env("POSTGRES_PORT", default="")
DB_NAME = env("POSTGRES_DB", default="")
DB_HOST = env("POSTGRES_HOST", default="")
DB_CONFIG_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASES = {"default": env.dj_db_url("DATABASE_URL", default=DB_CONFIG_URL)}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
{%- else %}
DATABASES = {}
{%- endif %}
{%- if cookiecutter.use_django_channels == 'y' %}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": env.list("CHANNEL_LAYERS_HOSTS")},
    }
}
{%- endif %}


# GENERAL
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "UTC"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
{%- if cookiecutter.postgresql_version == 'No database' %}


# SESSION
# ------------------------------------------------------------------------------
# django.contrib.sessions.backends.file
# django.contrib.sessions.backends.cache
# django.contrib.sessions.backends.signed_cookies
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
{%- endif %}


# TEMPLATES
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [APPS_DIR / "shared" / "templates"],
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                {%- if cookiecutter.postgresql_version != 'No database' %}
                "django.contrib.auth.context_processors.auth",
                {%- endif %}
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Your stuff: custom template context processors go here
            ],
        },
    }
]
{%- if cookiecutter.use_django_rest_framework == 'n' or cookiecutter.use_django_allauth == 'y' %}
# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"
{%- endif %}


# STATIC
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = {% if cookiecutter.use_django_storages == 'y' %}None{% else %}APPS_DIR / "static"{% endif %}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (APPS_DIR / "shared" / "static",)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# MEDIA
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = APPS_DIR / "shared" / "media"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


# URLs
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
# Location of root django.contrib.admin URL, use {% raw %}{% url 'admin:index' %}{% endraw %}
ADMIN_URL = "admin/"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"
{%- if cookiecutter.use_django_channels == 'y' %}
ASGI_APPLICATION = "config.routing.application"
{%- endif %}


# PASSWORD HASHING
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
{%- if cookiecutter.postgresql_version != 'No database' %}


# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [  # fmt: off
    "django.contrib.auth.backends.ModelBackend"{%- if cookiecutter.use_django_allauth == 'y' %},{%- endif %}  # fmt: off
    {%- if cookiecutter.use_django_allauth == 'y' %}
    "allauth.account.auth_backends.AuthenticationBackend",  # fmt: off
    {%- endif %}
]  # fmt: off
{%- if cookiecutter.use_django_allauth == 'y' %}

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_ADAPTER = "{{cookiecutter.project_slug}}.users.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "{{cookiecutter.project_slug}}.users.adapters.SocialAccountAdapter"
{%- endif %}

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "users:redirect"
LOGIN_URL = "account_login"
{%- endif %}


# SLUGIFIER
# ------------------------------------------------------------------------------
AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
{%- if cookiecutter.use_celery == 'y' %}


# CELERY
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["config.celery.CeleryConfig"]

if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="django://")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_SOFT_TIME_LIMIT = 60
{%- endif %}


# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    {%- if cookiecutter.postgresql_version != 'No database' %}
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    {%- endif %}
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        {%- if cookiecutter.postgresql_version != 'No database' %}
        "rest_framework.authentication.BasicAuthentication",
        {%- endif %}
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "SEARCH_PARAM": "search",
    "ORDERING_PARAM": "ordering",
    "COERCE_DECIMAL_TO_STRING": True,
    "UNAUTHENTICATED_USER": None,
}
{%- if cookiecutter.use_graphql == 'y' %}

# OpenAPI Schema location
OPENAPI_SCHEMA_DIR = APPS_DIR / "schema"
OPENAPI_SCHEMA_FILENAME = "schema.yml"
OPENAPI_SCHEMA_URL = "docs/swagger.json"
OPENAPI_SCHEMA_VIEW_NAME = "openapi-schema-json"


# GRAPHQL (GRAPHENE)
# ------------------------------------------------------------------------------
GRAPHENE = {
    "SCHEMA": "config.schema.schema"  # Where your Graphene
    # schema lives
}
{%- endif %}


DJANGO_CHECK_MIGRATION = env.bool('DJANGO_CHECK_MIGRATION', default=False)

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
