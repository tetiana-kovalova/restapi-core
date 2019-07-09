import os

from datetime import datetime


class Settings(object):
    instance = None

    IS_JENKINS = False

    TESTS_PATH = 'tests'
    BASE_URL = 'https://restful-booker.herokuapp.com'

    COMMAND_EXECUTOR = ''
    ALLURE_RESULTS_PATH = ''

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Settings, cls).__new__(cls)

            if cls.IS_JENKINS:
                cls.API_RESULTS_PATH = 'api_results'
            else:
                api_results_dir = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                cls.API_RESULTS_PATH = os.path.join(os.environ.get('USERPROFILE'), 'api_results', api_results_dir)

            cls.ALLURE_RESULTS_PATH = os.path.join(cls.API_RESULTS_PATH, 'allure')

            for folder in [cls.API_RESULTS_PATH, cls.ALLURE_RESULTS_PATH]:
                try:
                    os.makedirs(folder, 0o777)
                    os.chmod(folder, 0o777)
                    print('- bash       | makedirs %s' % folder)
                except OSError:
                    os.chmod(folder, 0o777)
                    print('- bash       | chmod %s' % folder)

            print('')

        return cls.instance
