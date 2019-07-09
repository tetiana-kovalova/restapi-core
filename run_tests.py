import os
import sys

import nose

from settings import Settings

if __name__ == '__main__':
    module = 'tests'

    allure_folder, result_folder = Settings().ALLURE_RESULTS_PATH, Settings().API_RESULTS_PATH

    for folder in [allure_folder, result_folder]:
        try:
            os.makedirs(folder, 0o777)
            os.chmod(folder, 0o777)
            print(f'- bash       | makedirs {folder}')
        except OSError:
            os.chmod(folder, 0o777)
            print(f'- bash       | chmod  {folder}')
    print('')

    argv = [sys.argv[0],
            '--verbosity=0',
            '--nocapture',
            '--logging-level=WARN',
            '--logging-filter=browser',
            '--with-xunit',
            f'--xunit-file={result_folder}/nosetests.xml',
            '--with-allure',
            f'--logdir={allure_folder}',
            '--not-clear-logdir',
            module]

    nose.run(argv=argv)

    os.system(f'cd {Settings().ALLURE_RESULTS_PATH} && allure generate . && allure open -p 5000')
