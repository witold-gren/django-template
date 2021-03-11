{% if 'alpine' in cookiecutter.python_version %}#!/bin/sh{% else %}#!/usr/bin/env bash{% endif %}

set -o errexit
set -o pipefail
set -o nounset


cmd="$@"

# We only want to run pytest with an explicitly set django settings module
PYTEST="pytest"

# Command which will be run to perform CI
RUNTEST="$PYTEST --cov --cov-report xml \
    --verbose

# --pylama \
# --isort \
# --black"

{%- if cookiecutter.postgresql_version != 'No database' %}
migrate() {
    python manage.py migrate --noinput
}
{%- endif %}
collectstatic() {
    python manage.py collectstatic --clear --no-input
}

validate_spec() {
    python -m openapi_spec_validator schema/schema.yml
}
{%- if cookiecutter.postgresql_version != 'No database' %}
check_migrations() {
    python manage.py makemigrations --check --dry-run
}
check_applied_migrations() {
    python manage.py checkmigrations
}
{%- endif %}
lint() {
    pylama
    isort --check-only --atomic .
    black --check .
}

shell() {
    python manage.py shell
}

ishell() {
    python manage.py shell_plus --ipython
}
{%- if cookiecutter.postgresql_version != 'No database' %}
postgres_ready() {
    python << END
import sys
import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}")
except psycopg2.OperationalError:
    sys.exit(-1)

sys.exit(0)
END
}


counter=0
until postgres_ready; do
  >&2 echo 'PostgreSQL is unavailable (sleeping)...'
  sleep 1
  if [ $counter -gt "60" ]; then
    echo "Can't connect to PostgreSQL. Exiting."
    exit 1
  fi
  counter=$(expr $counter + 1)
done

>&2 echo 'PostgreSQL is up - continuing...'


# Check current migration. This is important when we apply new version of app and usage Job object in kubernetes.
# We must wain before we run our new version of app, K8S object Job must be completed by applying all migrations.
if [ -z ${DJANGO_CHECK_MIGRATION+x} ]; then
  echo 'Skip check migrations - continuing...'
else
  if [ "$DJANGO_CHECK_MIGRATION" = 'True' ]; then
    counter=0
    until check_applied_migrations; do
      >&2 echo 'Django migrations was not applied (sleeping)...'
      sleep 1
      if [ $counter -gt "60" ]; then
        echo "Waiting too long to apply Django migration. Exiting."
        exit 1
      fi
      counter=$(expr $counter + 1)
    done

    >&2 echo 'Django migrations was checked - continuing...'
  else
    echo 'Check migrations was disabled - continuing...'
  fi
fi

{%- endif %}


case "$cmd" in
    {%- if cookiecutter.postgresql_version != 'No database' %}
    check_migrations)
        check_migrations
    ;;{%- endif %}
    lint)
        lint
    ;;
    sort)
        isort -rc --atomic .
    ;;
    format)
        black .
    ;;
    test)
        ${PYTEST}
    ;;
    runtest)
        lint{%- if cookiecutter.postgresql_version != 'No database' %}
        check_migrations{%- endif %}
        validate_spec
        ${RUNTEST}
    ;;
    runcitest)
        pipenv install --dev
        lint{%- if cookiecutter.postgresql_version != 'No database' %}
        check_migrations{%- endif %}
        validate_spec
        ${RUNTEST}
    ;;
    lock-dependencies)
        # If we don't have a Pipfile.lock in the app directory, that means this is the
        # first build and we should use the one generated during the build
        if [ ! -f Pipfile.lock ]; then
            cp ${BUILD_PIPFILE_LOCK} Pipfile.lock
        else
          pipenv lock
        fi
    ;;
    {% if cookiecutter.postgresql_version != 'No database' %}
    migrate)
        migrate
    ;;{% endif %}
    collectstatic)
        collectstatic
    ;;
    shell)
        shell
    ;;
    ishell)
        ishell
    ;;
    jupyter)
        python manage.py shell_plus --notebook
    ;;
    builddoc)
        sphinx-build -a -b html -d /docs/build/doctrees /docs/source /docs/build/html
    ;;
    *)
        $cmd  # usage start.sh or gunicorn.sh
    ;;
esac
