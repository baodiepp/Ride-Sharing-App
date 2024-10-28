"""Dispatcher for the simulation"""

from typing import Optional
from driver import Driver
from passenger import Passenger


class Dispatcher:
    """A dispatcher fulfills requests from passengers and drivers for a
    ride-sharing service.

    When a passenger requests a driver, the dispatcher assigns a driver to the
    passenger. If no driver is available, the passenger is placed on a waiting
    list for the next available driver. A passenger that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a passenger, the dispatcher assigns a passenger from
    the waiting list to the driver. If there is no passenger on the waiting list
    the dispatcher does nothing. Once a driver requests a passenger, the driver
    is registered with the dispatcher, and will be used to fulfill future
    passenger requests.

    === Private Attributes ===
    _drivers:
        A dictionary whose key is driver.id, and value is the driver
    _waiting_passengers:
        A list of passengers waiting to be assigned a driver.
    """

    _drivers: dict[str, Driver]
    _waiting_passengers: list[Passenger]

    def __init__(self) -> None:
        """Initialize a Dispatcher.

        """
        self._drivers = {}
        self._waiting_passengers = []

    def __str__(self) -> str:
        """Return a string representation.

        """
        return f'The dictionary of drivers: {self._drivers} \n' \
               f'The list of waiting passengers: {self._waiting_passengers}'

    def request_driver(self, passenger: Passenger) -> Optional[Driver]:
        """Return a driver for the passenger, or None if no driver is available.

        Add the passenger to the waiting list if there is no available driver.

        """
        available_drivers = [self._drivers[drivers] for drivers in self._drivers
                             if self._drivers[drivers].is_idle]
        if not available_drivers:
            self._waiting_passengers.append(passenger)
            return None

        fastest_driver = available_drivers[0]
        min_time = fastest_driver.get_travel_time(passenger.origin)

        for driver in available_drivers:
            if driver.get_travel_time(passenger.origin) < min_time:
                min_time = driver.get_travel_time(passenger.origin)
                fastest_driver = driver
        return fastest_driver

    def request_passenger(self, driver: Driver) -> Optional[Passenger]:
        """Return a passenger for the driver, or None if no passenger is
        available.

        If this is a new driver, register the driver for future passenger
        requests.

        """
        if driver.id not in self._drivers:
            self._drivers[driver.id] = driver

        if passengers := self._waiting_passengers:
            waiting_passenger = passengers[0]
            passengers.remove(waiting_passenger)
            return waiting_passenger

        return None

    def cancel_ride(self, passenger: Passenger) -> None:
        """Cancel the ride for passenger.

        """
        if passenger in self._waiting_passengers:
            self._waiting_passengers.remove(passenger)
        return None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={'extra-imports': ['typing', 'driver', 'passenger']})
