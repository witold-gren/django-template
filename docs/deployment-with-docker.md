Deployment with Docker
======================

Prerequisites
-------------

* Docker (at least 1.10)
* Docker Compose (at least 1.6)

Understand the Compose Setup
----------------------------

Before you start, check out the `production.yml` file in the root of this project. 
This is where each component of this application gets its configuration from. 
Notice how it provides configuration for these services:

* `postgres` service that runs the database
* `redis` for caching
* `django` is the Django project run by gunicorn

If you chose the `use_celery` option, there are two more services:

* `celeryworker` which runs the celery worker process
* `celerybeat` which runs the celery beat process


Populate .env With Your Environment Variables
---------------------------------------------

Some of these services rely on environment variables set by you. There is an 
`env.example` file in the root directory of this project as a starting point. 
Add your own variables to the file and rename it to `.env`. This file won't be 
tracked by git by default so you'll have to make sure to use some other 
mechanism to copy your secret if you are relying solely on git.

It is **highly recommended** that before you build your production application, 
you set your POSTGRES_USER value here. This will create a non-default user for 
the postgres image. If you do not set this user before building the application, 
the default user 'postgres' will be created, and this user will not be able to 
create or restore backups.

To obtain logs and information about crashes in a production setup, make sure 
that you have access to an external Sentry instance (e.g. by creating an account 
with [sentry.io]), and set the `DJANGO_SENTRY_DSN` variable. This should be 
enough to report crashes to Sentry.

[sentry.io](https://sentry.io/welcome)

Run your app with docker-compose
--------------------------------

To get started, pull your code from source control (don't forget the `.env` 
file) and change to your projects root directory.

You'll need to build the stack first. To do that, run::

    $ docker-compose -f docker-compose.prod.yml build

Once this is ready, you can run it with::

    $ docker-compose -f docker-compose.prod.yml up

To run a migration, open up a second terminal and run::

    $ docker-compose -f docker-compose.prod.yml run django python manage.py migrate

To create a superuser, run::

    $ docker-compose -f docker-compose.prod.yml run django python manage.py createsuperuser

If you need a shell, run::

    $ docker-compose -f docker-compose.prod.yml run django python manage.py shell

To get an output of all running containers.

To check your logs, run::

    $ docker-compose -f docker-compose.prod.yml logs

If you want to scale your application, run::

    $ docker-compose -f docker-compose.prod.yml scale django=4
    $ docker-compose -f docker-compose.prod.yml scale celeryworker=2

Warning: Don't run the scale command on postgres or celerybeat.

If you have errors, you can always check your stack with `docker-compose`. 
Switch to your projects root directory and run::

    $ docker-compose -f docker-compose.prod.yml ps


Jenkins and Continuous Delivery
-------------------------------

TODO: devops describe
