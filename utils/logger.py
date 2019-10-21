import logging
import os

from settings import Settings


class BaseLogger(object):
    logger = None
    log_path = Settings.RESULTS_PATH
    allure_path = os.path.join(log_path, 'allure')

    def __new__(cls):
        if cls.logger is None:
            cls.logger = logging.getLogger(__name__)

            # Create folder for logger records
            for folder in [cls.log_path, cls.allure_path]:
                try:
                    os.makedirs(folder, 0o777)
                    os.chmod(folder, 0o777)
                    print('- bash       | makedirs %s' % folder)
                except OSError:
                    os.chmod(folder, 0o777)
                    print('- bash       | chmod %s' % folder)

            # Create handler
            f_handler = logging.FileHandler(os.path.join(cls.log_path, 'test_results.log'))
            f_handler.setLevel(logging.INFO)

            # Create formatters and add it to handlers
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            cls.logger.addHandler(f_handler)

            cls.logger.setLevel(logging.DEBUG)

        return cls.logger
