{%- if cookiecutter.use_django_rest_framework == 'y' -%}
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
{%- else -%}
import pytest
{%- endif %}
{%- if cookiecutter.use_django_rest_framework == 'n' %}

from {{cookiecutter.project_slug}}.users.views import UserRedirectView, UserUpdateView
{%- else %}

from {{cookiecutter.project_slug}}.users import serializers, views
{%- endif %}
{%- if cookiecutter.use_django_rest_framework == 'n' %}


class TestUserRedirectView:
    @pytest.mark.django_db
    def test_get_redirect_url(self, user_instance, rf):
        # Instantiate the view directly. Never do this outside a test!
        view = UserRedirectView()
        # Generate a fake request
        request = rf.get("/fake-url")
        # Attach the user to the request
        request.user = user_instance
        # Attach the request to the view
        view.request = request
        # Expect: url for user instance fixture, as that is the request's user object
        assert view.get_redirect_url() == f"/users/{user_instance.username}/"


class TestUserUpdateView:
    @pytest.mark.django_db
    def test_get_success_url(self, user_instance, rf):
        # Instantiate the view directly. Never do this outside a test!
        view = UserUpdateView()
        # Generate a fake request
        request = rf.get("/fake-url")
        # Attach the user to the request
        request.user = user_instance
        # Attach the request to the view
        view.request = request
        # Expect: url for user instance fixture, as that is the request's user object
        assert view.get_success_url() == f"/users/{user_instance.username}/"

    @pytest.mark.django_db
    def test_get_object(self, user_factory, rf):
        # Create a User object
        user = user_factory.create()
        # Instantiate the view directly. Never do this outside a test!
        view = UserUpdateView()
        # Generate a fake request
        request = rf.get("/fake-url")
        # Attach the user to the request
        request.user = user
        # Attach the request to the view
        view.request = request
        # Expect: user instance fixture, as that is the request's user object
        assert view.get_object() == user
{%- else %}


class TestUserViewSet:
    def test_serializer_list_of_users(self, admin_user, rf, user_factory):
        view = views.UserViewSet.as_view({"get": "list"})

        users = user_factory.build_batch(5)
        views.UserViewSet.queryset = users
        request = rf.get("/users/")
        force_authenticate(request, user=admin_user)
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == len(users)
        assert (
            response.data.get("results")
            == serializers.UserSerializer(users, many=True).data
        )

    @patch.object(views.UserViewSet, "get_object")
    def test_serializer_detail_of_users(self, mock_views, admin_user, rf):
        view = views.UserViewSet.as_view({"get": "retrieve"})

        mock_views.return_value = admin_user
        request = rf.get(f"/users/{admin_user.id}/")
        force_authenticate(request, user=admin_user)
        response = view(request, pk=1)

        assert mock_views.called
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializers.UserSerializer(admin_user).data
{%- endif %}
