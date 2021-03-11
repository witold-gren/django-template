"""
Test a single configuration from a json config file.
"""
import pytest

from .docker_compose_executor import docker_services, DockerComposeRuntimeError


@pytest.mark.usefixtures("cookiecutter_project")
def test_configuration(
    project_compose_file, cleanup_docker_images, configuration, docker_pypi_mirror
):
    """
    Test if docker container can be built and basic tests pass for a given configuration.
    """
    docker_build_args = (
        {"PIPENV_PYPI_MIRROR": docker_pypi_mirror} if docker_pypi_mirror else None
    )

    # run the actual tests
    with docker_services(
        project_compose_file,
        remove_images=False,
        docker_build_args=docker_build_args,
    ) as docker_compose:
        docker_compose.execute(["run", "app", "runtest"])

    # Here we'd like to see if all the containers actually start. This is a test
    # for Celery, Flower, and any related service configurations. Since we
    # can't easily check if everything is actually up or just starting,
    # we set a best-effort timeout and catch the exception explicitly
    with docker_services(
        project_compose_file,
        remove_images=cleanup_docker_images,
        docker_build_args=docker_build_args,
        timeout=30,
    ) as docker_compose:
        try:
            docker_compose.execute(["up", "--abort-on-container-exit"])
        except DockerComposeRuntimeError as exc:
            assert "returned -9" in str(exc)
