"""
Does the following:

1. Generates and saves random secret key
2. Removes the taskapp if celery isn't going to be used
3. Removes the .idea directory if PyCharm isn't going to be used
4. Copy files from /docs/ to {{ cookiecutter.project_slug }}/docs/
5. Removes {{ cookiecutter.project_slug }}/backend/{{ cookiecutter.project_slug }}/schema.py if GraphQL (graphene) isn't
   going to be used

    TODO: this might have to be moved to a pre_gen_hook

A portion of this code was adopted from Django's standard crypto functions and
utilities, specifically:
    https://github.com/django/django/blob/master/django/utils/crypto.py
"""
import os
import random
import shutil
import string

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


def get_random_string(length=50):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    punctuation = string.punctuation.replace('"', "").replace("'", "")
    punctuation = punctuation.replace("\\", "")
    if using_sysrandom:
        return "".join(
            random.choice(string.digits + string.ascii_letters + punctuation)
            for i in range(length)
        )

    print(
        "Cookiecutter Django couldn't find a secure pseudo-random number generator on your system."
        " Please change change your SECRET_KEY variables in conf/settings/local.py and env.example"
        " manually."
    )
    return "CHANGEME!!"


def set_secret_key(setting_file_location, placeholder="!!!SET DJANGO_SECRET_KEY!!!"):
    # Open locals.py
    with open(setting_file_location) as f:
        file_ = f.read()

    # Generate a SECRET_KEY that matches the Django standard
    SECRET_KEY = get_random_string()

    # Replace "CHANGEME!!!" with SECRET_KEY
    file_ = file_.replace(placeholder, SECRET_KEY, 1)

    # Write the results to the locals.py module
    with open(setting_file_location, "w") as f:
        f.write(file_)


def make_secret_key(project_directory):
    """Generates and saves random secret key"""
    # Determine the local env file location
    local_env_file = os.path.join(project_directory, ".envs/.local/.django")

    # replace the key in the local env file
    set_secret_key(local_env_file)

    # Determine the production env file location
    production_env_file = os.path.join(project_directory, ".envs/.production/.django")

    # env.example file
    set_secret_key(production_env_file)


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def remove_pycharm_dir(project_directory):
    """
    Removes directories related to PyCharm
    if it isn't going to be used
    """
    idea_dir_location = os.path.join(PROJECT_DIRECTORY, ".idea/")
    if os.path.exists(idea_dir_location):
        shutil.rmtree(idea_dir_location)

    docs_dir_location = os.path.join(PROJECT_DIRECTORY, "docs/pycharm/")
    if os.path.exists(docs_dir_location):
        shutil.rmtree(docs_dir_location)


def remove_db_files():
    """
    Remove all files related to the database. Used for cases where a database
    is not used.
    """
    # Delete the contrib/sites app
    sites_relative_dir = "backend/{{cookiecutter.project_slug}}/contrib/sites/"
    sites_absolute_dir = os.path.join(PROJECT_DIRECTORY, sites_relative_dir)
    shutil.rmtree(sites_absolute_dir, ignore_errors=True)

    # Delete the users app
    users_relative_dir = "backend/{{cookiecutter.project_slug}}/users/"
    users_absolute_dir = os.path.join(PROJECT_DIRECTORY, users_relative_dir)
    shutil.rmtree(users_absolute_dir, ignore_errors=True)

    # Delete the postgres .env files
    envs_dir = os.path.join(PROJECT_DIRECTORY, ".envs")
    for subdir in (".local", ".production"):
        env_file_path = os.path.join(envs_dir, subdir, ".postgres")
        remove_file(env_file_path)


def remove_copying_files():
    """
    Removes files needed for the GPLv3 licence if it isn't going to be used
    """
    for filename in ["COPYING"]:
        os.remove(os.path.join(PROJECT_DIRECTORY, filename))


def remove_drf_files(project_directory):
    """
    Removes files from DRF like serializers oraz test_serializers
    """
    for filename in [
        "backend/{{ cookiecutter.project_slug }}/users/serializers.py",
        "backend/{{ cookiecutter.project_slug }}/users/tests/test_serializers.py",
    ]:
        os.remove(os.path.join(PROJECT_DIRECTORY, "", filename))


def remove_taskapp(project_directory):
    """
    Removes Celery app
    """
    os.remove(os.path.join(PROJECT_DIRECTORY, "config/celery.py"))


def remove_docs_dir(project_directory):
    """
    Removes documentation folder and files
    """
    docs_dir_location = os.path.join(PROJECT_DIRECTORY, "docs/")
    if os.path.exists(docs_dir_location):
        shutil.rmtree(docs_dir_location)


def remove_templates(project_directory):
    for path in [
        "shared/templates/bootstrap4/",
        "shared/templates/pages/",
        "shared/templates/users/",
    ]:
        path_location = os.path.join(PROJECT_DIRECTORY, path)
        if os.path.exists(path_location):
            shutil.rmtree(path_location)
    templates_path = os.path.join(project_directory, "shared/templates")
    template_files = ["403_csrf.html", "404.html", "500.html", "base.html"]
    for filename in template_files:
        filepath = os.path.join(templates_path, filename)
        remove_file(filepath)


def remove_auth_configuration(project_directory):
    adapters = "backend/{{ cookiecutter.project_slug }}/users/adapters.py"
    path_adapters = os.path.join(PROJECT_DIRECTORY, adapters)
    remove_file(path_adapters)

    test_adapters = (
        "backend/{{ cookiecutter.project_slug }}/users/tests/test_adapters.py"
    )
    path_test_adapters = os.path.join(PROJECT_DIRECTORY, test_adapters)
    remove_file(path_test_adapters)

    account_folder = os.path.join(PROJECT_DIRECTORY, "shared/templates/account")
    shutil.rmtree(account_folder)


def remove_django_channels_configuration(project_directory):
    asgi = "backend/config/asgi.py"
    path_asgi = os.path.join(PROJECT_DIRECTORY, asgi)
    remove_file(path_asgi)

    routing = "backend/config/routing.py"
    path_routing = os.path.join(PROJECT_DIRECTORY, routing)
    remove_file(path_routing)

    routing = "docker/production/backend/daphne.sh"
    path_routing = os.path.join(PROJECT_DIRECTORY, routing)
    remove_file(path_routing)


def remove_graphene_files():
    """
    Removes files related to django-graphene.
    """
    for filename in [
        "backend/config/schema.py",
        "backend/{{ cookiecutter.project_slug }}/users/schema.py",
        "backend/{{ cookiecutter.project_slug }}/users/tests/test_query.py",
    ]:
        filepath = os.path.join(PROJECT_DIRECTORY, "", filename)
        remove_file(filepath)


# Generates and saves random secret key
make_secret_key(PROJECT_DIRECTORY)

# Removes the .idea directory if PyCharm isn't going to be used
if "{{ cookiecutter.use_pycharm }}".lower() != "y":
    remove_pycharm_dir(PROJECT_DIRECTORY)

# Removes files needed for the GPLv3 licence if it isn't going to be used.
if "{{ cookiecutter.open_source_license}}" != "GPLv3":
    remove_copying_files()

# Removed all files from Django Rest Framework
if "{{ cookiecutter.use_django_rest_framework }}".lower() != "y":
    remove_drf_files(PROJECT_DIRECTORY)
else:
    remove_templates(PROJECT_DIRECTORY)

# Remove all Celery files if we're not using it
if "{{ cookiecutter.use_celery }}".lower() != "y":
    remove_taskapp(PROJECT_DIRECTORY)

# Remove documentation if you don't need
if "{{ cookiecutter.use_sphinx }}".lower() != "y":
    remove_docs_dir(PROJECT_DIRECTORY)

# Remove django_allauth configuration if you don't need
if "{{ cookiecutter.use_django_allauth }}".lower() != "y":
    remove_auth_configuration(PROJECT_DIRECTORY)

# Remove django_channels configuration if you don't need
if "{{ cookiecutter.use_django_channels }}".lower() != "y":
    remove_django_channels_configuration(PROJECT_DIRECTORY)

# Remove django_storages configuration if you don't need
if "{{ cookiecutter.use_django_storages }}".lower() != "y":
    storages = "backend/config/storages.py"
    path_storages = os.path.join(PROJECT_DIRECTORY, storages)
    remove_file(path_storages)

# Remove sites migration when don't usage database
if "{{ cookiecutter.postgresql_version }}" == "No database":
    remove_db_files()

# Remove files related to django-graphene if GraphQL isn't going to be used
if "{{ cookiecutter.use_graphql }}".lower() != "y":
    remove_graphene_files()
