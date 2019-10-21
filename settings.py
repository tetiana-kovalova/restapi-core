from datetime import datetime
import os


class Settings:
    BASE_URL = 'https://restful-booker.herokuapp.com'
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    RESULTS_PATH = os.path.join(os.environ.get('USERPROFILE'), 'test_results', datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
