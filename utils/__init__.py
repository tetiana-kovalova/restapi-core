import nose

try:
    # noinspection PyUnresolvedReferences
    step = nose.allure.step
    # noinspection PyUnresolvedReferences
    feature = nose.allure.feature
    # noinspection PyUnresolvedReferences
    issue = nose.allure.issue
    # noinspection PyUnresolvedReferences
    attach = nose.allure.attach
    # noinspection PyUnresolvedReferences
    environment = nose.allure.environment
except (AttributeError, ImportError):
    def options():
        def decorator(target):
            return target
        return decorator
    step = options
