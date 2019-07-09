import inspect
import re

from utils import step

TEST_CLASS_COUNTER = 1


class BaseTest(object):

    @classmethod
    def setup_class(cls):
        global TEST_CLASS_COUNTER
        print('\n%02d. %s\n' % (TEST_CLASS_COUNTER, re.sub(r"(\w)([A-Z])", r"\1 \2", cls.__name__).upper().replace('TEST ', '')))
        TEST_CLASS_COUNTER += 1

    @classmethod
    def teardown(cls):
        errors = [fi.frame.f_locals['outcome'].errors for fi in inspect.stack() if 'outcome' in fi.frame.f_locals][-1]
        if len(errors) > 0:
            test, last_error = errors[-1]
            exception = last_error[1]

            with step('FAILED'):
                print(f'- FAILED with {type(exception).__name__}\n')
        else:
            print('- PASSED\n')
