"""
Generate test configurations for template tests. A template tests builds
a docker container for the given configuration and then runs application
tests in it. This module is used to create said configurations, and optionally
save them into .json files in a directory, so test execution can be parallelized
more easily.
"""

import argparse
import functools
import itertools
import json
import os
import pathlib
import random
import sys
import uuid
from typing import Any, Dict, Generator, Iterable, List, Union

# Seed random for consistent results
random.seed(0)

# These multiple-choice options are ignored when generating test configurations
IGNORED_MULTI_OPTIONS = ("open_source_license",)

# Number of random sets of binary settings we generate for each base
BINARY_CONFIGURATION_COUNT = 3

CookiecutterJson = Dict[str, Union[str, List[str]]]


def get_default_configuration(cookiecutter_json: CookiecutterJson) -> Dict[str, str]:
    """
    Get the default values for the cookiecutter configuration.
    """
    default_options = dict()
    for key, value in cookiecutter_json.items():
        if isinstance(value, str) and "{{" not in value:  # ignore templated values
            default_options[key] = value
        elif isinstance(value, list):
            assert len(value) > 0, "Option list must have at least one element"
            default_options[key] = value[0]
    return default_options


def get_binary_choice_variables(cookiecutter_json: CookiecutterJson) -> List[str]:
    return [key for key, value in cookiecutter_json.items() if value in ("y", "n")]


def get_multiple_choice_options(
    cookiecutter_json: CookiecutterJson
) -> Dict[str, List[str]]:
    variables = {
        key: value
        for key, value in cookiecutter_json.items()
        if isinstance(value, list) and key not in IGNORED_MULTI_OPTIONS
    }
    return variables


def cartesian_product_dict(
    **kwargs: Iterable[Any]
) -> Generator[Dict[str, Any], None, None]:
    keys, vals = kwargs.keys(), kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def make_variable_options(
    multi_options: Dict[str, List[str]], binary_variables: List[str]
) -> Generator[Dict[str, str], None, None]:
    all_configurations = cartesian_product_dict(**multi_options)

    # First take all the possible configurations of multi-choice options
    # and switch all the binary options on
    for configuration in all_configurations:
        configuration = {
            **configuration,
            **dict(zip(binary_variables, itertools.repeat("y"))),
        }
        if configuration["postgresql_version"] == "No database":
            # some options don't work without a db
            configuration["use_django_allauth"] = "n"
            configuration["use_graphql"] = "n"
        yield configuration

    # Set the multi-choice options to default values
    multi_options["python_version"][2:] = []
    multi_options["postgresql_version"][1:] = []

    representative_configurations = cartesian_product_dict(**multi_options)

    # Try a couple random combinations of the binary-choice options
    # TODO: Make this more deterministic and clever
    for configuration in representative_configurations:
        for _ in range(BINARY_CONFIGURATION_COUNT):
            binary_conf = [random.choice("yn") for _ in binary_variables]
            yield {**configuration, **dict(zip(binary_variables, binary_conf))}


@functools.lru_cache(maxsize=1)
def load_cookiecutter_json() -> Dict[str, Any]:
    PROJECT_ROOT = pathlib.Path(__file__).parents[1]
    cookiecutter_json_path = PROJECT_ROOT / "cookiecutter.json"
    with cookiecutter_json_path.open() as json_file:
        cookiecutter_json = json.load(json_file)
    return cookiecutter_json


def generate_project_name() -> str:
    short_uid = uuid.uuid4().hex[:8]
    return f"project_{short_uid}"


def make_configurations() -> Generator[Dict[str, str], None, None]:
    cookiecutter_json = load_cookiecutter_json()

    default_configuration = get_default_configuration(cookiecutter_json)
    multi_choice_options = get_multiple_choice_options(cookiecutter_json)
    binary_choice_variables = get_binary_choice_variables(cookiecutter_json)

    for options in make_variable_options(multi_choice_options, binary_choice_variables):
        yield {
            **default_configuration,
            **options,
            "project_name": generate_project_name(),
        }


def main(output_directory: str) -> None:
    for i, options in enumerate(make_configurations()):
        output_file = os.path.join(output_directory, f"config-{i}.json")

        with open(output_file, "w+") as f:
            f.write(json.dumps(options))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate cookiecutter configurations for testing purposes."
    )
    parser.add_argument("output_directory", type=str)

    args = parser.parse_args()
    output_directory = args.output_directory

    try:
        test_file_path = os.path.join(output_directory, "test")
        with open(test_file_path, "w+") as f:
            f.write("test")
        os.remove(test_file_path)
    except IOError:
        print("Directory is not writable", file=sys.stderr)
        exit(1)

    main(output_directory)
