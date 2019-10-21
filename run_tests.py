import os
import sys

import pytest
from utils.logger import BaseLogger

if __name__ == '__main__':

    module = 'tests'

    argv = [sys.argv[0],
            '--verbosity=0',
            '--show-capture=stdout',
            f'--alluredir={BaseLogger.allure_path}',
            module]

    pytest.main(args=argv)

    os.system(f'cd {BaseLogger.allure_path} && allure generate . && allure open -p 5000')

