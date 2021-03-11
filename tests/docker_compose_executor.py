"""
Wrapper for running docker-compose in a subprocess. Used for template tests.
"""

import os
import pathlib
import subprocess
from contextlib import contextmanager
from typing import Container, Generator, List, Optional, Union


class DockerComposeRuntimeError(RuntimeError):
    pass


class DockerComposeExecutor:
    def __init__(self, compose_file: str, timeout: int) -> None:
        self._compose_file = compose_file
        self._timeout = timeout

    def execute(self, subcommand: Union[str, List[str]]) -> str:
        subcommand = [subcommand] if isinstance(subcommand, str) else subcommand
        command = ["docker-compose", "-f", self._compose_file, *subcommand]
        return self._execute(command)

    def _execute(
        self, command: List[str], success_codes: Container[int] = (os.EX_OK,)
    ) -> str:
        # Run in the compose file's folder as you normally would when building
        # This also helps with some of compose's quirks, like the inability to
        # specify a .env file location
        cwd = pathlib.Path(self._compose_file).parent
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=self._timeout,
                cwd=cwd,
            )
        except subprocess.TimeoutExpired as exc:
            exit_code = -9
            output = exc.output
        else:
            exit_code = result.returncode
            output = result.stdout.decode("utf-8")
        if exit_code not in success_codes:
            raise DockerComposeRuntimeError(
                f"Command {command} returned {exit_code}:\n {output}."
            )
        return output


@contextmanager
def docker_services(
    yml_file_abs_path: str,
    timeout: int = 1800,
    remove_images: bool = True,
    docker_build_args: Optional[dict] = None,
) -> Generator[DockerComposeExecutor, None, None]:
    docker_build_args = docker_build_args or {}
    build_command = ["build"]
    for key, value in docker_build_args.items():
        build_command.extend(["--build-arg", f"{key}={value}"])
    docker_compose = DockerComposeExecutor(yml_file_abs_path, timeout)

    try:
        docker_compose.execute(build_command)
        yield docker_compose
    finally:
        cleanup_cmd = ["down", "-v"]
        if remove_images:
            cleanup_cmd.extend(["--rmi", "local"])
        docker_compose.execute(cleanup_cmd)
