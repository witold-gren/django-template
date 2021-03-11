{%- if cookiecutter.use_graphql == 'y' -%}
from django.urls import reverse

{% endif -%}
import pytest

{% if cookiecutter.use_graphql == 'y' -%}
from config.schema import schema
{% endif -%}
from faker import config

{%- if cookiecutter.use_graphql == 'y' %}
from graphene.test import Client
{%- endif %}
from pytest_django.lazy_django import skip_if_no_django

{%- if cookiecutter.postgresql_version != 'No database' %}
from pytest_factoryboy import register
{%- endif %}
from requests_mock import MockerCore

{%- if cookiecutter.use_django_rest_framework == 'y' %}
from rest_framework.test import APIRequestFactory
{%- endif %}

{%- if cookiecutter.postgresql_version != 'No database' %}
from {{cookiecutter.project_slug}}.users.tests.factories import UserFactory
{%- endif %}

config.DEFAULT_LOCALE = "pl_PL"
{%- if cookiecutter.postgresql_version != 'No database' %}
register(UserFactory)
{%- endif %}


@pytest.fixture(scope="session")
def faker_locale():
    return "pl_PL"


@pytest.fixture(scope="session")
def setup_view():
    """Returns function able to setup Django's view.

    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to ``reverse()``

    Examples
    ========
    `setup_view` should be used as normal pytest's fixture::

        def test_hello_view(setup_view):
            name = 'django'
            request = RequestFactory().get('/fake-path')
            view = HelloView(template_name='hello.html')
            view = setup_view(view, request, name=name)

            # Example test ugly dispatch():
            response = view.dispatch(view.request, *view.args, **view.kwargs)
    """

    def _inner_setup_view(view, request, *args, **kwargs):
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    return _inner_setup_view


{%- if cookiecutter.use_django_rest_framework == 'y' %}
@pytest.fixture(scope="session")
def api_setup_view():
    """Returns function able to setup DRF's view.

    Examples
    ========
    `api_setup_view` should be used as normal pytest's fixture::

        def test_profile_info_view(api_setup_view):
            request = HttpRequest()
            view = views.ProfileInfoView()
            view = api_setup_view(view, request, 'list')
            assert view.get_serializer_class() == view.serializer_class
    """

    def _inner_api_setup_view(view, request, action, *args, **kwargs):
        view.request = request
        view.action = action
        view.args = args
        view.kwargs = kwargs
        return view

    return _inner_api_setup_view


@pytest.fixture()
def api_rf():
    """APIRequestFactory instance"""
    skip_if_no_django()
    return APIRequestFactory()
{%- endif %}


@pytest.yield_fixture(scope="session")
def requests_mock():
    mock = MockerCore()
    mock.start()
    yield mock
    mock.stop()

{%- if cookiecutter.use_graphql == 'y' %}
@pytest.fixture
def gql_client(rf):
    def inner(**kwargs):
        request = rf.get(reverse("graphql"))
        kwargs["context_value"] = request
        client = Client(schema, **kwargs)
        return client

    return inner
{%- endif %}

{%- if cookiecutter.postgresql_version != 'No database' %}
@pytest.fixture
def user_instance(user_factory):
    return user_factory.build()

@pytest.fixture
def admin_user_instance(user_factory):
    return user_factory.build(is_staff=True, is_superuser=True)
{%- endif %}

@pytest.fixture(autouse=True)
def temporary_media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = str(tmpdir)