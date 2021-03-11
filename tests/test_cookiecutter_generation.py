"""
Cookiecutter project generation tests using pytest.
"""

import os
import re

import pytest
import sh
from binaryornot.check import is_binary
import json

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths(paths):
    """Method to check all paths have correct substitutions,
    used by other tests cases
    """
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue
        for line in open(path, "r"):
            match = RE_OBJ.search(line)
            msg = "cookiecutter variable not replaced in {}"
            assert match is None, msg.format(path)


@pytest.fixture
def custom_template(tmpdir, configuration):
    """ prepare custom templates based on configurations """

    configuration["repo_name"] = configuration["project_name"],
    template = tmpdir.ensure("cookiecutter-template", dir=True)
    template.join("cookiecutter.json").write(json.dumps(configuration))

    repo_dir = template.ensure("{{cookiecutter.repo_name}}", dir=True)
    repo_dir.join("README.rst").write("{{cookiecutter.repo_name}}")

    return template


def test_custom_configurations(cookies, custom_template, configuration):
    """ use custom templates created from configuration fixtures
    to check if cookiecutter can build project without actually building it """
    result = cookies.bake(template=str(custom_template))
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == configuration["project_name"]
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)

