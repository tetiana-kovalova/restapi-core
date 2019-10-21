import json
import os
from pathlib import Path

import allure
from deepdiff import DeepDiff
from jsonschema import validate

from settings import Settings


@allure.step('Utils > JSON > Compare JSON objects')
def compare(expected, actual, exclude_paths=None):
    return DeepDiff(expected, actual, exclude_paths=exclude_paths, ignore_order=True)


@allure.step('Utils > JSON > Validate JSON object according to schema file [{1}]')
def validate_schema(actual, schema_file):
    with open(os.path.join(Settings.PROJECT_PATH, Path(f'resources/expected_schema/{schema_file}'))) as filename:
        expected_schema = json.loads(filename.read())
        return validate(actual, expected_schema)
