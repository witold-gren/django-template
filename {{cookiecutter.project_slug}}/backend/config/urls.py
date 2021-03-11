import os

from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
{%- if cookiecutter.use_django_rest_framework == 'n' %}
from django.views.generic import TemplateView
{%- else %}

from {{cookiecutter.project_slug }}.utils.views import OpenAPISchemaView, ReDocView
{%- if cookiecutter.use_graphql == 'y' %}
from graphene_django.views import GraphQLView
{%- endif %}
from rest_framework import authentication, permissions
{%- endif %}

urlpatterns = [
    path("healthz/", include("health_check.urls")),
    {%- if cookiecutter.use_django_rest_framework == 'n' %}
    path("$", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/$",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    {%- endif %}
    {%- if cookiecutter.postgresql_version != 'No database' %}
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("{{cookiecutter.project_slug}}.users.urls")),
    {%- if cookiecutter.use_django_allauth == 'y' %}
    path("accounts/", include("allauth.urls")),
    {%- endif %}
    {%- endif %}
    {%- if cookiecutter.use_django_rest_framework == 'y' %}
    {%- if cookiecutter.postgresql_version != 'No database' %}
    path("rest-auth/", include("rest_auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    {%- endif %}
    path(
        rf"^{settings.OPENAPI_SCHEMA_URL}$",
        OpenAPISchemaView.as_view(),
        name=settings.OPENAPI_SCHEMA_VIEW_NAME,
    ),
    path("docs/$", ReDocView.as_view(), name="redoc"),
    {%- endif %}
    {%- if cookiecutter.use_graphql == 'y' %}
    path("graphql/", GraphQLView.as_view(graphiql=True), name="graphql"),
    {%- endif %}
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production":
    urlpatterns += [path("prometheus/", include("django_prometheus.urls"))]
