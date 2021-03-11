Project Generation Options
==========================

project_name [project_name]:
    Your human-readable project name, including any capitalization or spaces.

project_slug [project_name]:
    The slug of your project, without dashes or spaces. Used to name your repo
    and in other places where a Python-importable version of your project name
    is needed.

author_name [Your Name]:
    You! This goes into places like the LICENSE file.

email [Your email]:
    Your email address.

description [A short description of the project.]
    Used in the generated README.rst and other places.

domain_name [example.com]
    Whatever domain name you plan to use for your project when it goes live.

slack_channel [project_slug]
    Name of slack channel when Jenkins send notifications.

use_celery [y]
    Full configuration for asynchronous task execution by Celery

use_django_rest_framework [y]
    Full configuration Django Rest Framework with generating documentation.

version [0.1.0]
    The starting version number for your project.

use_pycharm [n]
    Adds support for developing in [PyCharm] with a preconfigured .idea directory.

windows [n]
    Whether you'll be developing on Windows.

postgresql_version [1]
    Version of PostgreSQL who will be install
    
    1. 11.6
    2. 10.11
    3. 9.6

python_version [1]
    Version of Python who will be install
    
    1. 3.7-slim
    2. 3.7-alpine

django_version [1]
    Select version of Django who will be install in your project.
    
    1. 2.2

open_source_license [1]
    Select a software license for the project. The choices are:

    1. MIT
    2. BSD
    3. GPLv3
    4. Apache Software License 2.0
    5. Not open source
