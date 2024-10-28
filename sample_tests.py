import pytest

from location import Location, deserialize_location
from event import create_event_list, PassengerRequest, DriverRequest, Pickup, \
    Dropoff, Cancellation
from monitor import Monitor
from dispatcher import Dispatcher
from simulation import Simulation


def test_location_print() -> None:
    """ Tests for the correct implementation of the creating and print of the
    Location class
    """
    location = Location(0, 0)
    assert str(location) == "(0, 0)"
    location2 = deserialize_location("2, 2")
    assert str(location2) == "(2, 2)"


def test_event_creation() -> None:
    """ Test for correct implementation of the event creations

    """
    events = create_event_list("events.txt")
    assert (len(events), 12)
    for event in events:
        instance = isinstance(event, PassengerRequest) or \
                   isinstance(event, DriverRequest)
        assert (instance, True)

    driverRequest = events[0]
    assert driverRequest.timestamp == 0
    passengerRequest = events[-1]
    assert passengerRequest.timestamp == 25


def test_simulation_run() -> None:
    """Test simulation run on a basic set of events"""
    events = create_event_list("events.txt")

    assert len(events) == 12
    sim = Simulation()
    report = sim.run(events)
    assert len(report) == 3
    assert report['average_passenger_wait_time'] == pytest.approx(0.5)
    assert report['average_driver_total_distance'] == pytest.approx(4.5)
    assert report['average_driver_trip_distance'] == pytest.approx(
        3.8333333333333335)


def test_simulation_run2() -> None:
    """Test simulation run on a basic set of events"""
    events = create_event_list("even more events.txt")

    assert len(events) == 15
    sim = Simulation()
    report = sim.run(events)
    assert len(report) == 3
    assert report['average_passenger_wait_time'] == pytest.approx(1.8)
    assert report['average_driver_total_distance'] == pytest.approx(4.5)
    assert report['average_driver_trip_distance'] == pytest.approx(
        3.8333333333333335)


def test_simulation_run3() -> None:
    """Test simulation run on a basic set of events"""
    events = create_event_list("even more events.txt")

    # assert len(events) == 15
    sim = Simulation()
    report = sim.run(events)
    assert len(report) == 3
    assert report['average_passenger_wait_time'] == pytest.approx(1.8)
    assert report['average_driver_total_distance'] == pytest.approx(4.5)
    assert report['average_driver_trip_distance'] == pytest.approx(
        3.8333333333333335)

def test_special_events() -> None:
    """Test Cancellation and Pickup on a basic set of events"""

    # Environment Setup
    events = create_event_list("events.txt")
    dvr_request, psg_request = events[0], events[-1]
    driver, passenger = dvr_request.driver, psg_request.passenger
    monitor = Monitor()
    dispatcher = Dispatcher()
    dvr_request.do(dispatcher, monitor)
    psg_request.do(dispatcher, monitor)

    # Testing
    trip = Pickup(0, passenger, driver)
    dropoff = trip.do(dispatcher, monitor)

    assert isinstance(dropoff[0], Dropoff) == True
    assert passenger.status == 'satisfied'

    # ES
    events = create_event_list("events.txt")
    dvr_request, psg_request = events[1], events[-2]
    driver, passenger = dvr_request.driver, psg_request.passenger
    monitor = Monitor()
    dispatcher = Dispatcher()
    dvr_request.do(dispatcher, monitor)
    psg_request.do(dispatcher, monitor)

    # Testing
    cancel = Cancellation(0, passenger)
    result = cancel.do(dispatcher, monitor)
    assert result == []
    assert passenger.status == 'cancelled'


if __name__ == '__main__':
    pytest.main(['sample_tests.py'])
