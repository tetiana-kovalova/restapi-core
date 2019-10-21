import random
from datetime import datetime, timedelta

import allure
import pytest

from data_objects.booking_data import Booking
from methods import booking
from utils import test_data_loader, json_validator


class TestBooking:
    test_ids, input_data = test_data_loader.load_test_data('booking.yaml')

    @allure.step('Test > TestBooking > Test Data Preparation')
    @pytest.fixture(params=input_data, ids=test_ids)
    def test_data_preparation(self, request):
        data = request.param
        test_data = Booking(data)
        booking_id = booking.create_booking(test_data.booking)[0]['bookingid']
        yield test_data, booking_id

    @allure.feature('Booking > Test Create Booking')
    def test_1_create_booking(self, test_data_preparation):
        test_data = test_data_preparation[0]

        actual_booking, status_code = booking.create_booking(test_data.booking)

        with allure.step("Assert HTTP Status code and Response content"):
            assert status_code == 200, f'Unexpected HTTP Status code: {status_code}. Expected: 200'
            assert not json_validator.compare(test_data.booking, actual_booking['booking'], test_data.ignored)
            assert not json_validator.validate_schema(actual_booking, 'create_booking.json')

    @allure.feature('Booking > Test Get Booking')
    def test_2_get_booking(self, test_data_preparation):
        test_data, booking_id = test_data_preparation

        actual_booking, status_code = booking.get_booking(booking_id)

        with allure.step("Assert HTTP Status code and Response content"):
            assert status_code == 200, f'Unexpected HTTP Status code: {status_code}. Expected: 200'
            assert not json_validator.compare(test_data.booking, actual_booking, test_data.ignored)
            assert not json_validator.validate_schema(actual_booking, 'get_booking.json')

    @allure.feature('Booking > Test Get All Bookings')
    def test_3_get_all_bookings(self, test_data_preparation):
        booking_id = test_data_preparation[1]

        bookings, status_code = booking.get_all_bookings()

        with allure.step("Assert HTTP Status code and Response content"):
            assert status_code == 200, f'Unexpected HTTP Status code: {status_code}. Expected: 200'
            assert booking_id in [b['bookingid'] for b in bookings]

    @allure.feature('Booking > Test Update Booking')
    def test_4_update_booking(self, test_data_preparation):
        test_data, booking_id = test_data_preparation
        test_data.booking['firstname'] = f'New Test Name {random.choice(range(1000))}'
        test_data.booking['lastname'] = f'New Test Lastname {random.choice(range(1000))}'
        test_data.booking['bookingdates']['checkin'] = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')
        test_data.booking['bookingdates']['checkout'] = (datetime.today() + timedelta(days=60)).strftime('%Y-%m-%d')
        test_data.booking['totalprice'] = random.choice(range(1000))
        test_data.booking['depositpaid'] = random.choice([False, True])
        test_data.booking['additionalneeds'] = f'New Test Additional Needs {random.choice(range(1000))}'

        actual_booking, status_code = booking.update_booking(booking_id, test_data.booking)

        with allure.step("Assert HTTP Status code and Response content"):
            assert status_code == 200, f'Unexpected HTTP Status code: {status_code}. Expected: 200'
            assert not json_validator.compare(test_data.booking, actual_booking, test_data.ignored)
            assert not json_validator.validate_schema(actual_booking, 'get_booking.json')

    @allure.feature('Booking > Test Update Booking')
    def test_5_update_booking_partially(self, test_data_preparation):
        test_data, booking_id = test_data_preparation
        test_data.booking['depositpaid'] = random.choice([False, True])
        test_data.booking['additionalneeds'] = None

        actual_booking, status_code = booking.update_booking(booking_id, test_data.booking)

        with allure.step("Assert HTTP Status code and Response content"):
            assert status_code == 200, f'Unexpected HTTP Status code: {status_code}. Expected: 200'
            assert not json_validator.compare(test_data.booking, actual_booking, test_data.ignored)
            assert not json_validator.validate_schema(actual_booking, 'get_booking.json')

    @allure.feature('Booking > Test Delete Booking')
    def test_6_delete_booking(self, test_data_preparation):
        booking_id = random.choice([b['bookingid'] for b in booking.get_all_bookings()[0]])

        actual_booking, status_code = booking.delete_booking(booking_id)

        with allure.step("Assert HTTP Status code and Request result"):
            assert status_code == 201, f'Unexpected HTTP Status code: {status_code}. Expected: 201'
            assert booking_id not in [b['bookingid'] for b in booking.get_all_bookings()[0]]
