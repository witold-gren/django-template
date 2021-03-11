{% if 'alpine' in cookiecutter.python_version %}#!/bin/sh{% else %}#!/usr/bin/env bash{% endif %}
# https://docs.celeryproject.org/en/latest/userguide/workers.html

set -o errexit
set -o pipefail
set -o nounset

celery -A {{cookiecutter.project_slug}}.taskapp worker \
        --loglevel=${CELERY_LEVEL:-INFO} \
        --concurrency=${CELERY_CONCURRENCY:-2}
