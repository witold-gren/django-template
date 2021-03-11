import json
import os

import pytest
import yaml
from cookiecutter.main import cookiecutter

from . import COOKIECUTTER_ROOT
from .generate_configurations import make_configurations

CONFIGURATION_FIXTURE_NAME = "generated_configuration"


def pytest_addoption(parser):
    parser.addoption(
        "--config-file",
        action="store",
        default=None,
        help="Only run a test for the config in this file",
    )
    parser.addoption(
        "--no-docker-image-cleanup",
        action="store_true",
        default=False,
        help="Don't clean up docker images after compose tests. Speeds up"
        "test execution, but requires manual cleanup afterwards.",
    )
    parser.addoption(
        "--docker-pypi-mirror",
        action="store",
        help="Set a PyPI mirror for building docker containers via "
        "compose. Note that containers are built with network=host, "
        "so localhost will work, for example.",
    )


def pytest_generate_tests(metafunc):
    """
    If a configuration file path was passed as a command line parameter, only
    use that value for the `configuration` fixture. Otherwise, parametrize
    every test that uses this fixture with all the generated configurations.
    """
    if CONFIGURATION_FIXTURE_NAME in metafunc.fixturenames:
        config_file_path = metafunc.config.option.config_file
        if config_file_path is not None:
            with open(config_file_path) as fp:
                configuration = json.load(fp)
            configurations = [configuration]
        else:
            configurations = make_configurations()

        metafunc.parametrize(CONFIGURATION_FIXTURE_NAME, configurations)


@pytest.fixture
def configuration(generated_configuration):
    """
    We can modify the generated configurations a bit before feeding them to
    cookiecutter.
    """
    return generated_configuration


@pytest.fixture
def project_name(configuration):
    """
    We need unique project names, as docker resource names are derived from them, and
    those need to be unique for the whole host OS. Currently, we rely on the configuration
    generator to provide these.
    """
    return configuration["project_name"]


@pytest.fixture
def project_root(tmpdir, project_name):
    return tmpdir / project_name


@pytest.fixture
def cleanup_docker_images(request):
    """
    Whether we clean up docker images after a template test. Caching helps tests run
    faster, but targetted cleaning up after a full run is difficult.
    """
    return not request.config.getoption("--no-docker-image-cleanup")


@pytest.fixture
def docker_pypi_mirror(request):
    """
    Use this value as a PyPI mirror for containers built by compose, if it's set.
    """
    return request.config.getoption("--docker-pypi-mirror")


@pytest.fixture
def cookiecutter_project(tmpdir, project_root, configuration):
    cookiecutter(
        COOKIECUTTER_ROOT, no_input=True, extra_context=configuration, output_dir=tmpdir
    )
    # Set a UID in the .env file before building to handle docker permissions
    env_file_path = project_root / ".env"
    with open(env_file_path, "w+") as fp:
        fp.write(f"UID={os.getuid()}")


@pytest.fixture
def project_compose_file(project_root):
    # Here, we remove any port bindings from the compose file. Tests can bring up
    # the whole stack and can run in parallel, wherein static port bindings would
    # cause `docker-compose up` to fail.
    compose_path = project_root / "docker-compose.yml"
    with open(compose_path) as fp:
        compose_spec = yaml.safe_load(fp)
    for service_spec in compose_spec["services"].values():
        if "ports" in service_spec:
            del service_spec["ports"]
    with open(compose_path, "w+") as fp:
        yaml.safe_dump(compose_spec, fp)
    return compose_path
