from nose.tools import assert_equals

from models import Booking
from tests import BaseTest
from utils import feature


class TestBooking(BaseTest):

    @feature('Booking > Test Get All Bookings')
    def test_1_get_all_bookings(self):
        booking = Booking()
        content, status_code = booking.get_all_bookings()
        assert_equals(status_code, 200)

        booking_ids = [obj.bookingid for obj in content]
        assert_equals([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], sorted(booking_ids))

    @feature('CS > Test Get Booking')
    def test_2_get_booking(self):
        booking = Booking(2, 'Jim', 'Ericsson', '2017-08-06', '2019-02-12', 318)
        content, status_code = booking.get_booking(booking.bookingid)
        assert_equals(status_code, 200)
        assert_equals(content.firstname, booking.firstname)
        assert_equals(content.lastname, booking.lastname)
        assert_equals(content.bookingdates.checkin, booking.checkin)
        assert_equals(content.bookingdates.checkout, booking.checkout)
        assert_equals(content.totalprice, booking.totalprice)
