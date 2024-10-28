import pytest

from location import Location, deserialize_location
from event import create_event_list, PassengerRequest, DriverRequest, Pickup, \
    Dropoff, Cancellation
from monitor import Monitor
from dispatcher import Dispatcher
from simulation import Simulation
from random import randrange
import names


def create_tests():
    x = open('inf', 'w')
    i = 1
    while i <= 15:
        x.write(
            f'{randrange(0, 11)} DriverRequest {names.get_first_name()} '
            f'{randrange(1, 51)},{randrange(1, 51)} {randrange(1, 16)}\n')
        i += 1
    x.write('\n')
    x.write('\n')
    x.write('\n')
    x.write('\n')
    x.write('\n')
    k = 0
    while k <= 15:
        x.write(
            f'{randrange(0, 11)} PassengerRequest {names.get_first_name()} '
            f'{randrange(1, 51)},{randrange(1, 51)} {randrange(1, 51)},'
            f'{randrange(1, 51)} {randrange(1, 16)}\n')
        k += 1


def runsim():
    events = create_event_list('inf')
    sim = Simulation()
    stats = sim.run(events)
    print(stats)


counter = 0
while counter <= 5:
    create_tests()
    runsim()
