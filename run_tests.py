import datetime
import os
import sys

import nose

if __name__ == '__main__':
    module = 'tests'

    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    allure_folder, result_folder = f'{now}/allure', f'{now}/result'

    for folder in [allure_folder, result_folder]:
        try:
            os.makedirs(folder, 0o777)
            os.chmod(folder, 0o777)
            print('- bash | makedirs %s' % folder)
        except OSError:
            os.chmod(folder, 0o777)
            print('- bash | chmod %s' % folder)
    print('')

    argv = [sys.argv[0],
            '--verbosity=0',
            '--nocapture',
            '--logging-level=WARN',
            '--logging-filter=browser',
            '--with-xunit',
            '--xunit-file=%s/nosetests.xml' % result_folder,
            '--with-allure',
            '--logdir=%s' % allure_folder,
            '--not-clear-logdir',
            module]

    nose.run(argv=argv)

    os.system(f'cd {allure_folder} && allure generate . && allure open -p 5000')
