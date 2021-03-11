import sys

project_slug = "{{ cookiecutter.project_slug }}"

if hasattr(project_slug, "isidentifier"):
    assert (
        project_slug.isidentifier()
    ), "Project slug should be valid Python identifier!"

python_version = "{{ cookiecutter.python_version }}"
django_version = "{{ cookiecutter.django_version }}"
django_channels = "{{ cookiecutter.use_django_channels }}"


if (
    "{{ cookiecutter.use_django_allauth }}" == "y"
    and "{{ cookiecutter.postgresql_version }}" == "No database"
):
    sys.stdout.write("ERROR: django-allauth requires a database.")
    sys.exit(1)

if (
    "{{ cookiecutter.use_graphql }}" == "y"
    and "{{ cookiecutter.postgresql_version }}" == "No database"
):
    sys.stdout.write("ERROR: GraphQL requires a database.")
    sys.exit(1)
