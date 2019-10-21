import allure

from constants import Method
from methods import Rest


@allure.step('Rest > Get All Bookings')
def get_all_bookings():
    return Rest().send(Method.GET, 'booking')


@allure.step('Rest > Get Booking [id={0}]')
def get_booking(booking_id):
    return Rest().send(Method.GET, f'booking/{booking_id}')


@allure.step('Rest > Create Booking')
def create_booking(booking):
    return Rest().send(Method.POST, 'booking', booking)


@allure.step('Rest > Update Booking [id={0}]')
def update_booking(booking_id, booking):
    return Rest().send(Method.PUT, f'booking/{booking_id}', booking)


@allure.step('Rest > Delete Booking [id={0}]')
def delete_booking(booking_id):
    return Rest().send(Method.DELETE, f'booking/{booking_id}')
