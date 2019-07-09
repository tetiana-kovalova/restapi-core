import os
import sys

import nose

from settings import Settings

if __name__ == '__main__':
    module = 'tests'

    argv = [sys.argv[0],
            '--verbosity=0',
            '--nocapture',
            '--logging-level=WARN',
            '--logging-filter=browser',
            '--with-xunit',
            f'--xunit-file={Settings().API_RESULTS_PATH}/nosetests.xml',
            '--with-allure',
            f'--logdir={Settings().ALLURE_RESULTS_PATH}',
            '--not-clear-logdir',
            module]

    nose.run(argv=argv)

    os.system(f'cd {Settings().ALLURE_RESULTS_PATH} && allure generate . && allure open -p 5000')
