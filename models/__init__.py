from constants import Service
from services import REST_PREFIX, Rest

from utils import step


class Booking(Rest):
    def __init__(self, bookingid=None, firstname=None, lastname=None, checkin=None, checkout=None, totalprice=None):
        self.bookingid = bookingid
        self.firstname = firstname
        self.lastname = lastname
        self.checkin = checkin
        self.checkout = checkout
        self.totalprice = totalprice

    @step('Rest > Get All Bookings')
    def get_all_bookings(self):
        print(f'{REST_PREFIX} Get All Bookings')
        return self.service(Service.GET, 'booking')

    @step('Rest > Get Booking')
    def get_booking(self, bookingid):
        print(f'{REST_PREFIX} Get Booking [id = {bookingid}]')
        return self.service(Service.GET, f'booking/{bookingid}')
