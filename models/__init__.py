from constants import Service
from services import REST_PREFIX, Rest

from utils import step


class Booking(Rest):
    def __init__(self,
                 bookingid=None,    firstname=None,     lastname=None,      checkin=None, checkout=None,
                 totalprice=0,      depositpaid=True,   additionalneeds=None):

        self.bookingid = bookingid
        self.firstname = firstname
        self.lastname = lastname
        self.checkin = checkin
        self.checkout = checkout
        self.totalprice = totalprice
        self.depositpaid = depositpaid
        self.additionalneeds = additionalneeds

    @step('Rest > Get All Bookings')
    def get_all_bookings(self):
        print(f'{REST_PREFIX} GET All Bookings')
        return self.service(Service.GET, 'booking')

    @step('Rest > Get Booking [id={1}]')
    def get_booking(self, bookingid):
        print(f'{REST_PREFIX} GET Booking [id={bookingid}]')
        return self.service(Service.GET, f'booking/{bookingid}')

    @step('Rest > Create Booking')
    def create_booking(self, booking):
        print(f'{REST_PREFIX} POST Booking')

        data = {"firstname":        booking.firstname,
                "lastname":         booking.lastname,
                "totalprice":       booking.totalprice,
                "depositpaid":      booking.depositpaid,
                "bookingdates": {
                    "checkin":      booking.checkin,
                    "checkout":     booking.checkout
                    },
                "additionalneeds":  booking.additionalneeds}

        return self.service(Service.POST, 'booking', data)

    @step('Rest > Update Booking')
    def update_booking(self, booking):
        print(f'{REST_PREFIX} PUT Booking')

        data = {"firstname":        booking.firstname,
                "lastname":         booking.lastname,
                "totalprice":       booking.totalprice,
                "depositpaid":      booking.depositpaid,
                "bookingdates": {
                    "checkin":      booking.checkin,
                    "checkout":     booking.checkout
                    },
                "additionalneeds":  booking.additionalneeds}

        return self.service(Service.PUT, f'booking/{booking.bookingid}', data)

    @step('Rest > Delete Booking [id={1}]')
    def delete_booking(self, bookingid):
        print(f'{REST_PREFIX} DELETE Booking [id={bookingid}]')
        return self.service(Service.DELETE, f'booking/{bookingid}')
