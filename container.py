"""Containers of objects"""


class Container:
    """A container that holds objects.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def add(self, item: object) -> None:
        """Add <item> to this Container.

        """
        raise NotImplementedError("Implemented in a subclass")

    def remove(self) -> object:
        """Remove and return a single item from this Container.

        """
        raise NotImplementedError("Implemented in a subclass")

    def is_empty(self) -> bool:
        """Return True iff this Container is empty.

        """
        raise NotImplementedError("Implemented in a subclass")


class PriorityQueue(Container):
    """A queue of items that operates in priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first. Ties are resolved in FIFO order,
    meaning the item which was inserted *earlier* is the first one to be
    removed.

    Priority is defined by the rich comparison methods for the objects in the
    container (__lt__, __le__, __gt__, __ge__).

    If x < y, then x has a *HIGHER* priority than y.

    All objects in the container must be of the same type.
    """

    # === Private Attributes ===
    _items: list
    #     The items stored in the priority queue.
    #
    # === Representation Invariants ===
    # _items is a sorted list, where the first item in the queue is the
    # item with the highest priority.

    def __init__(self) -> None:
        """Initialize an empty PriorityQueue.

        """
        self._items = []

    def remove(self) -> object:
        """Remove and return the next item from this PriorityQueue.

        Precondition: <self> should not be empty.

        >>> pq = PriorityQueue()
        >>> pq.add("red")
        >>> pq.add("blue")
        >>> pq.add("yellow")
        >>> pq.add("green")
        >>> pq.remove()
        'blue'
        >>> pq.remove()
        'green'
        >>> pq.remove()
        'red'
        >>> pq.remove()
        'yellow'
        """
        return self._items.pop(0)

    def is_empty(self) -> bool:
        """
        Return true iff this PriorityQueue is empty.

        >>> pq = PriorityQueue()
        >>> pq.is_empty()
        True
        >>> pq.add("thing")
        >>> pq.is_empty()
        False
        """
        return len(self._items) == 0

    def add(self, item: object) -> None:
        """Add <item> to this PriorityQueue.
        >>> p = PriorityQueue()
        >>> p.add(1)
        >>> p.add(10)
        >>> p.add(5)
        >>> p.add(0)
        >>> p._items
        [0, 1, 5, 10]

        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> pq.add("red")
        >>> pq.add("green")
        >>> pq._items
        ['blue', 'green', 'red', 'yellow']
        """

        for i, obj in enumerate(self._items):
            if item < obj:
                self._items.insert(i, item)
                return None
        self._items.append(item)
        return None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
