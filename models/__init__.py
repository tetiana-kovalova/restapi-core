from nose.tools import assert_equals

from constants import Method
from methods import REST_PREFIX, Rest

from utils import step


class Booking(object):
    def __init__(self,
                 firstname=None,    lastname=None,      checkin=None,       checkout=None,
                 totalprice=0,      depositpaid=True,   additionalneeds=None):

        self.firstname = firstname
        self.lastname = lastname
        self.checkin = checkin
        self.checkout = checkout
        self.totalprice = totalprice
        self.depositpaid = depositpaid
        self.additionalneeds = additionalneeds

    @step('Assert booking fields')
    def assert_booking_fields(self, booking):
        for field, value in self.__dict__.items():
            with step(f'Assert field [{field}] value [{value}]'):
                if field in ['checkin', 'checkout']:
                    assert_equals(booking._asdict()['bookingdates']._asdict()[field], value,
                                  f"Actual value {booking._asdict()['bookingdates']._asdict()[field]} not equal to expected {value}")
                else:
                    assert_equals(booking._asdict()[field], value,
                                  f"Actual value [{booking._asdict()[field]}] not equal to expected [{value}]")


class BookingFactory(Rest):

    @step('Rest > Get All Bookings')
    def get_all_bookings(self):
        print(f'{REST_PREFIX} GET All Bookings')
        return self.send(Method.GET, 'booking')

    @step('Rest > Get Booking [id={1}]')
    def get_booking(self, bookingid):
        print(f'{REST_PREFIX} GET Booking [id={bookingid}]')
        return self.send(Method.GET, f'booking/{bookingid}')

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

        result, status_code = self.send(Method.POST, 'booking', data)

        return result.bookingid, result.booking, status_code

    @step('Rest > Update Booking [id={1}]')
    def update_booking(self, bookingid, booking):
        print(f'{REST_PREFIX} PUT Booking [id={bookingid}]')

        data = {"firstname":        booking.firstname,
                "lastname":         booking.lastname,
                "totalprice":       booking.totalprice,
                "depositpaid":      booking.depositpaid,
                "bookingdates": {
                    "checkin":      booking.checkin,
                    "checkout":     booking.checkout
                    },
                "additionalneeds":  booking.additionalneeds}

        return self.send(Method.PUT, f'booking/{bookingid}', data)

    @step('Rest > Delete Booking [id={1}]')
    def delete_booking(self, bookingid):
        print(f'{REST_PREFIX} DELETE Booking [id={bookingid}]')
        return self.send(Method.DELETE, f'booking/{bookingid}')
