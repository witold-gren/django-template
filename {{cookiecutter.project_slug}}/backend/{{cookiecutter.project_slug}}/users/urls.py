from django.conf.urls import url
{%- if cookiecutter.use_django_rest_framework == 'y' %}

from rest_framework import routers
{%- endif %}

from {{cookiecutter.project_slug}}.users import views

app_name = "users"

{%- if cookiecutter.use_django_rest_framework == 'n' %}
urlpatterns = [
    url(regex=r"^$", view=views.UserListView.as_view(), name="list"),
    url(regex=r"^~redirect/$", view=views.UserRedirectView.as_view(), name="redirect"),
    url(
        regex=r"^(?P<username>[\w.@+-]+)/$",
        view=views.UserDetailView.as_view(),
        name="detail",
    ),
    url(regex=r"^~update/$", view=views.UserUpdateView.as_view(), name="update"),
]
{%- else %}
router = routers.DefaultRouter()
router.register("", views.UserViewSet)
urlpatterns = router.urls
{%- endif %}