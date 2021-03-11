from django.urls import resolve, reverse

import pytest
{%- if cookiecutter.use_django_rest_framework == 'y' %}

from {{cookiecutter.project_slug}}.users.views import UserViewSet
{%- endif %}


class TestUserURLs:
    """Test URL patterns for users app."""
    {%- if cookiecutter.use_django_rest_framework == 'n' %}

    @pytest.mark.parametrize(
        "url,url_name",
        [
            ("/users/", "users:list"),
            ("/users/~redirect/", "users:redirect"),
            ("/users/testuser/", "users:detail"),
            ("/users/~update/", "users:update"),
        ],
    )
    def test_users_views_resolve(self, url, url_name):
        assert resolve(url).view_name == url_name

    @pytest.mark.parametrize(
        "url_name,url_kwargs,url",
        [
            ("users:list", {}, "/users/"),
            ("users:redirect", {}, "/users/~redirect/"),
            ("users:detail", {"username": "testuser"}, "/users/testuser/"),
            ("users:update", {}, "/users/~update/"),
        ],
    )
    def test_users_views_reverse(self, url_name, url_kwargs, url):
        assert reverse(url_name, kwargs=url_kwargs) == url
    {%- else %}

    @pytest.mark.parametrize("url,view_class", [("/users/", UserViewSet)])
    def test_users_views_resolve(self, url, view_class):
        assert resolve(url).func.cls == view_class

    @pytest.mark.parametrize(
        "url_name,url_kwargs,url",
        [
            ("users:user-list", {}, "/users/"),
            ("users:user-detail", {"pk": 1}, "/users/1/"),
        ],
    )
    def test_users_views_reverse(self, url_name, url_kwargs, url):
        assert reverse(url_name, kwargs=url_kwargs) == url
    {%- endif %}
