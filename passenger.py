"""
The passenger module contains the Passenger class. It also contains
constants that represent the status of the passenger.

=== Constants ===
WAITING: A constant used for the waiting passenger status.
CANCELLED: A constant used for the cancelled passenger status.
SATISFIED: A constant used for the satisfied passenger status
"""

from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Passenger:

    """A passenger for a trip-sharing service.

    === Attributes ===
    id:
        A unique identifier for the passenger.
    patience:
        The amount of time the passenger will wait for a driver.
    origin:
        The initial location of the passenger.
    destination:
        The destination for the passenger.
    status:
        The current status of the passenger.

    === Representation Invariants ===
    -  status: "waiting" | "cancelled" | "satisfied"
    """
    id: str
    patience: int
    origin: Location
    destination: Location
    status: str

    def __init__(self, identifier: str, patience: int, origin: Location,
                 destination: Location) -> None:
        """Initialize a Passenger.

        """
        self.id = identifier
        self.patience = patience
        self.origin = origin
        self.destination = destination
        self.status = WAITING

    def __str__(self) -> str:
        return f'id: {self.id} \n' \
               f'patience: {self.patience} \n' \
               f'origin: {self.origin} \n' \
               f'destination:  {self.destination} \n' \
               f'status: {self.status}'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['location']})
