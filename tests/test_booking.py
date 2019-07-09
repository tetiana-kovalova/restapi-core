from nose.tools import assert_equals, assert_true, assert_in

from models import Booking
from tests import BaseTest
from utils import feature

bookingid = 0


class TestBooking(BaseTest):

    @feature('Booking > Test Create Booking')
    def test_1_create_booking(self):
        booking = Booking(firstname='Mary',     lastname='Smith',   checkin='2021-10-06', checkout='2025-10-06',
                          totalprice=100500,    depositpaid=True,   additionalneeds="Dry Towel")
        content, status_code = booking.create_booking(booking)
        assert_equals(status_code, 200)
        assert_equals(content.booking.firstname, booking.firstname)
        assert_equals(content.booking.lastname, booking.lastname)
        assert_equals(content.booking.bookingdates.checkin, booking.checkin)
        assert_equals(content.booking.bookingdates.checkout, booking.checkout)
        assert_equals(content.booking.totalprice, booking.totalprice)
        assert_true(isinstance(content.bookingid, int))

        global bookingid
        bookingid = content.bookingid

    @feature('Booking > Test Get Booking')
    def test_2_get_booking(self):
        booking = Booking(bookingid, 'Mary', 'Smith', '2021-10-06', '2025-10-06', 100500)
        content, status_code = booking.get_booking(booking.bookingid)
        assert_equals(status_code, 200)
        assert_equals(content.firstname, booking.firstname)
        assert_equals(content.lastname, booking.lastname)
        assert_equals(content.bookingdates.checkin, booking.checkin)
        assert_equals(content.bookingdates.checkout, booking.checkout)
        assert_equals(content.totalprice, booking.totalprice)

    @feature('Booking > Test Get All Bookings')
    def test_3_get_all_bookings(self):
        booking = Booking()
        content, status_code = booking.get_all_bookings()
        assert_equals(status_code, 200)

        booking_ids = [obj.bookingid for obj in content]
        assert_in(bookingid, booking_ids)

    @feature('Booking > Test Update Booking')
    def test_4_update_booking(self):
        booking = Booking(bookingid,             firstname='Nick',  lastname='Smith',   checkin='2021-10-06',
                          checkout='2021-11-06', totalprice=500,    depositpaid=False,  additionalneeds='Breakfast')
        content, status_code = booking.update_booking(booking)

        assert_equals(status_code, 200)
        assert_equals(content.booking.firstname, booking.firstname)
        assert_equals(content.booking.lastname, booking.lastname)
        assert_equals(content.booking.bookingdates.checkin, booking.checkin)
        assert_equals(content.booking.bookingdates.checkout, booking.checkout)
        assert_equals(content.booking.totalprice, booking.totalprice)
        assert_true(isinstance(content.bookingid, int))

    @feature('Booking > Test Get Booking')
    def test_5_get_booking(self):
        booking = Booking(bookingid, 'Nick', 'Smith', '2021-10-06', '2021-11-06', 500, False, 'Breakfast')
        content, status_code = booking.get_booking(booking.bookingid)

        assert_equals(status_code, 200)
        assert_equals(content.firstname, booking.firstname)
        assert_equals(content.lastname, booking.lastname)
        assert_equals(content.bookingdates.checkin, booking.checkin)
        assert_equals(content.bookingdates.checkout, booking.checkout)
        assert_equals(content.depositpaid, booking.depositpaid)
        assert_equals(content.additionalneeds, booking.additionalneeds)
