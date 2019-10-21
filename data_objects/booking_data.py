import random
from datetime import datetime, timedelta


class Booking:
    def __init__(self, test_data):

        self.firstname = test_data.get('firstname', 'Test Firstname')
        self.lastname = test_data.get('lastname', f'Test Lastname')
        self.checkin = test_data.get('bookingdates').get('checkin', datetime.today()).strftime('%Y-%m-%d')
        self.checkout = test_data.get('bookingdates').get('checkout', datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.totalprice = test_data.get('totalprice', random.choice(range(100, 999)))
        self.depositpaid = test_data.get('depositpaid', random.choice([True, False]))
        self.additionalneeds = test_data.get('additionalneeds', f'Test {datetime.now()}')

        self.booking = {'firstname':        self.firstname,
                        'lastname':         self.lastname,
                        'bookingdates':     {'checkin': self.checkin, 'checkout': self.checkout},
                        'totalprice':       self.totalprice,
                        'depositpaid':      self.depositpaid,
                        'additionalneeds':  self.additionalneeds}

        self.compare_content = test_data.get('compare', True)

        self.ignored = []  # ["root['id']"]
