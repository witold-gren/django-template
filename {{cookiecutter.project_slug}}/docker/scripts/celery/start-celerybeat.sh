{% if 'alpine' in cookiecutter.python_version %}#!/bin/sh{% else %}#!/usr/bin/env bash{% endif %}

set -o errexit
set -o pipefail
set -o nounset

celery -A {{cookiecutter.project_slug}}.taskapp beat -l INFO
