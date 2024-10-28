"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from __future__ import annotations
from typing import List
from passenger import Passenger, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, PASSENGER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    timestamp: A timestamp for this event.
    """

    timestamp: int

    def __init__(self, timestamp: int) -> None:
        """Initialize an Event with a given timestamp.

        Precondition: timestamp must be a non-negative integer.

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other: Event) -> bool:
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other: Event) -> bool:
        """Return True iff this Event is not equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other: Event) -> bool:
        """Return True iff this Event is less than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other: Event) -> bool:
        """Return True iff this Event is less than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other: Event) -> bool:
        """Return True iff this Event is greater than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other: Event) -> bool:
        """Return True iff this Event is greater than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        """
        raise NotImplementedError("Implemented in a subclass")


class PassengerRequest(Event):
    """A passenger requests a driver.

    === Attributes ===
    passenger: The passenger.
    """

    passenger: Passenger

    def __init__(self, timestamp: int, passenger: Passenger) -> None:
        """Initialize a PassengerRequest event.

        """
        super().__init__(timestamp)
        self.passenger = passenger

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Assign the passenger to a driver or add the passenger to a waiting
        list.
        If the passenger is assigned to a driver, the driver starts driving to
        the passenger.

        Return a Cancellation event. If the passenger is assigned to a driver,
        also return a Pickup event.

        """
        monitor.notify(self.timestamp, PASSENGER, REQUEST,
                       self.passenger.id, self.passenger.origin)

        events = []
        driver = dispatcher.request_driver(self.passenger)
        if driver is not None:
            travel_time = driver.start_drive(self.passenger.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 self.passenger, driver))
        events.append(Cancellation(self.timestamp + self.passenger.patience,
                                   self.passenger))
        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f"{self.timestamp} -- {self.passenger}: Request a driver"


class DriverRequest(Event):
    """A driver requests a passenger.

    === Attributes ===
    driver: The driver.
    """

    driver: Driver

    def __init__(self, timestamp: int, driver: Driver) -> None:
        """Initialize a DriverRequest event.

        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Register the driver, if this is the first request, and
        assign a passenger to the driver, if one is available.

        If a passenger is available, return a Pickup event.

        """
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)

        events = []
        passenger = dispatcher.request_passenger(self.driver)

        if passenger is not None:
            travel_time = self.driver.start_drive(passenger.origin)
            events.extend(
                (Pickup(self.timestamp + travel_time, passenger, self.driver),)
            )

        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f"{self.timestamp} -- {self.driver}: Request a passenger"


class Cancellation(Event):
    """
    Passenger cancels trip

    === Attributes ===
    passenger: the passenger

    """
    passenger: Passenger

    def __init__(self, timestamp: int, passenger: Passenger) -> None:
        super().__init__(timestamp)
        self.passenger = passenger

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f'{self.timestamp} -- {self.passenger}: Cancellation Event'

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """
        Changes a waiting passenger to a cancelled passenger

        """
        monitor.notify(self.timestamp, PASSENGER, CANCEL, self.passenger.id,
                       self.passenger.origin)

        if self.passenger.status == WAITING:
            self.passenger.status = CANCELLED
            dispatcher.cancel_ride(self.passenger)
        return []


class Pickup(Event):
    """
    A pickup event

    === Attributes ===
    driver: the driver
    passenger: the passenger
    """
    passenger: Passenger
    driver: Driver

    def __init__(
            self, timestamp: int, passenger: Passenger, driver: Driver) -> None:

        super().__init__(timestamp)
        self.passenger = passenger
        self.driver = driver

    def __str__(self) -> str:
        return f'{self.timestamp} -- {self.passenger} -- {self.driver}: ' \
               f'Pickup Event'

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """
        sets the driver’s location to the passenger’s location. If the passenger
        is waiting, the driver begins giving them a trip and the driver’s
        destination becomes the passenger’s destination.

        """
        self.driver.end_drive()
        self.driver.location = self.passenger.origin

        if self.passenger.status == WAITING:
            monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.id,
                           self.driver.location)
            monitor.notify(self.timestamp, PASSENGER, PICKUP, self.passenger.id,
                           self.passenger.origin)
            travel_time = self.driver.start_trip(self.passenger)
            self.passenger.status = SATISFIED
            return [Dropoff(
                self.timestamp + travel_time, self.driver, self.passenger)]

        elif self.passenger.status == CANCELLED:
            return [DriverRequest(self.timestamp, self.driver)]
        else:
            return []


class Dropoff(Event):
    """
    A drop off event

    === Attributes ===
    driver: the driver
    passenger: the passenger
    """
    driver: Driver
    passenger: Passenger

    def __init__(
            self, timestamp: int, driver: Driver, passenger: Passenger) -> None:
        super().__init__(timestamp)
        self.driver = driver
        self.passenger = passenger

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f'{self.timestamp} -- {self.driver} -- {self.passenger}: ' \
               f'Drop off Event '

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """
        A drop off event sets the driver’s location to the passenger’s
        destination. A new event for the driver requesting a passenger is
        scheduled to take place immediately, and the driver has no
        destination for the moment.
        """
        self.driver.location = self.passenger.destination

        monitor.notify(self.timestamp, DRIVER, DROPOFF, self.driver.id,
                       self.driver.location)
        self.driver.end_trip()
        return [DriverRequest(self.timestamp, self.driver)]


def create_event_list(filename: str) -> List[Event]:
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    filename: The name of a file that contains the list of events.
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'PassengerRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":
                driver = Driver(tokens[2], deserialize_location(tokens[3]),
                                int(tokens[4]))

                events.append(DriverRequest(timestamp, driver))

            elif event_type == "PassengerRequest":
                passenger = Passenger(tokens[2], int(tokens[5]),
                                      deserialize_location(tokens[3]),
                                      deserialize_location(tokens[4]))

                events.append(PassengerRequest(timestamp, passenger))

    return events


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={
            'allowed-io': ['create_event_list'],
            'extra-imports': ['passenger', 'dispatcher', 'driver',
                              'location', 'monitor']})
