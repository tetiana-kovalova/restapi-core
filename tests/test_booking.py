import random

from nose.tools import assert_equals, assert_true, assert_in, assert_not_in

from models import Booking, BookingFactory
from tests import BaseTest
from utils import feature

bookingid = 1


class TestBooking(BaseTest):

    @feature('Booking > Test Create Booking')
    def test_1_create_booking(self):
        global bookingid
        expected_booking = Booking(firstname='Mary',     lastname='Smith',   checkin='2021-10-06',  checkout='2025-10-06',
                                   totalprice=100500,    depositpaid=True,   additionalneeds='Dry Towel')

        bookingid, actual_booking, status_code = BookingFactory().create_booking(expected_booking)

        assert_equals(status_code, 200)
        expected_booking.assert_booking_fields(actual_booking)
        assert_true(isinstance(bookingid, int))

    @feature('Booking > Test Get Booking')
    def test_2_get_booking(self):
        expected_booking = Booking(firstname='Mary', lastname='Smith', checkin='2021-10-06', checkout='2025-10-06',
                                   totalprice=100500, depositpaid=True, additionalneeds='Dry Towel')

        actual_booking, status_code = BookingFactory().get_booking(bookingid)

        assert_equals(status_code, 200)
        expected_booking.assert_booking_fields(actual_booking)

    @feature('Booking > Test Get All Bookings')
    def test_3_get_all_bookings(self):
        bookings, status_code = BookingFactory().get_all_bookings()
        assert_equals(status_code, 200)

        booking_ids = [obj.bookingid for obj in bookings]
        assert_in(bookingid, booking_ids)

    @feature('Booking > Test Update Booking')
    def test_4_update_booking(self):
        expected_booking = Booking(firstname='Nick',  lastname='Smith',   checkin='2021-10-06', checkout='2021-11-06',
                                   totalprice=500,    depositpaid=False,  additionalneeds='Breakfast')

        actual_booking, status_code = BookingFactory().update_booking(bookingid, expected_booking)

        assert_equals(status_code, 200)
        expected_booking.assert_booking_fields(actual_booking)

    @feature('Booking > Test Delete Booking')
    def test_5_delete_booking(self):
        booking_id = random.choice([booking.bookingid for booking in BookingFactory().get_all_bookings()[0]])
        content, status_code = BookingFactory().delete_booking(booking_id)

        assert_equals(status_code, 201)
        assert_not_in(booking_id, [booking.bookingid for booking in BookingFactory().get_all_bookings()[0]])
