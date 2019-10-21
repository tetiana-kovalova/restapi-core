import os
from pathlib import Path

import yaml

from settings import Settings


class TestData(object):

    @classmethod
    def create_test_data(cls, file_names):
        ids, data = [], []
        file_names = file_names if isinstance(file_names, list) else [file_names]

        for file in file_names:
            with open(os.path.join(Settings.PROJECT_PATH, Path(file))) as f:
                test_data = yaml.safe_load(f)

                for i in test_data:
                    ids.append(i['id'])
                    data.append({k: v for k, v in i.items() if k != 'id'})

        return ids, data
