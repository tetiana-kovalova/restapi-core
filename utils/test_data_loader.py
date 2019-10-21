import os
from pathlib import Path

import allure
import yaml

from settings import Settings


@allure.step('Utils > TestDataLoader > Load Test Data from [{0}] file')
def load_test_data(file_names):
    ids, data = [], []
    file_names = file_names if isinstance(file_names, list) else [file_names]

    for file in file_names:
        with open(os.path.join(Settings.PROJECT_PATH, Path(f'resources/test_data/{file}'))) as f:
            test_data = yaml.safe_load(f)

            for i in test_data:
                ids.append(i['id'])

    return ids, test_data
