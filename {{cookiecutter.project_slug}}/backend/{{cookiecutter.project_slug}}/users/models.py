from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django_prometheus.models import ExportModelOperationsMixin


class User(
    ExportModelOperationsMixin("user"), AbstractUser
):  # By adding this mixin you can monitor with Prometheus
    # the creation/deletion/update rate for your model

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def __str__(self):
        return self.username
    {%- if cookiecutter.use_django_rest_framework == 'n' %}

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
    {%- endif %}
