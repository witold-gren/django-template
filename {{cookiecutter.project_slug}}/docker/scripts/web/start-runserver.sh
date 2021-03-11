{% if 'alpine' in cookiecutter.python_version %}#!/bin/sh{% else %}#!/usr/bin/env bash{% endif %}


set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


{% if cookiecutter.use_django_channels == 'y' %}python manage.py runserver 0.0.0.0:8000{% else %}python manage.py runserver_plus 0.0.0.0:8000 {% endif %}
