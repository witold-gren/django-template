{% if 'alpine' in cookiecutter.python_version %}#!/bin/sh{% else %}#!/usr/bin/env bash{% endif %}

set -o errexit
set -o pipefail
set -o nounset

#TODO: https://avilpage.com/2018/05/deploying-scaling-django-channels.html
/usr/local/bin/daphne -b 0.0.0.0 -p 8001 config.asgi:application
