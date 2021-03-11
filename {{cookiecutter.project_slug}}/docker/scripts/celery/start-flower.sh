{% if 'alpine' in cookiecutter.python_version %}#!/bin/sh{% else %}#!/usr/bin/env bash{% endif %}

set -o errexit
set -o nounset


celery flower \
    --app={{cookiecutter.project_slug}}.taskapp \
    --broker="${CELERY_BROKER_URL}" \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
