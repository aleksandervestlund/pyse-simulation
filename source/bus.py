import random
from collections.abc import Generator, Sequence
from dataclasses import dataclass

import numpy as np
from simpy import Environment, Timeout

from source.passenger import Passenger
from source.route import Route
from source.route_utils import Metric, pick_route


def find_end_stop(idx: int, start_stop: int) -> int:
    stop_table = {
        (1, 1): 4,
        (2, 3): 4,
        (1, 0): 3,
        (2, 2): 3,
        (3, 2): 2,
        (4, 3): 2,
        (3, 0): 1,
        (4, 1): 1,
    }
    return stop_table[(start_stop, idx)]


@dataclass(slots=True, frozen=True)
class Bus:
    env: Environment
    c: int
    number: int
    routes: Sequence[Route]
    q: float
    bus_utilisation: list[float]
    metric: Metric
    verbose: bool

    def __post_init__(self) -> None:
        self.env.process(self.drive())

    def drive(self) -> Generator[Timeout, None, None]:
        current_stop = random.randint(1, 4)
        west = current_stop in {1, 2}
        passengers: list[Passenger] = []

        while True:
            start_stop = current_stop
            west = not west
            idx = pick_route(
                current_stop, self.routes, self.env, self.metric, west
            )
            route = self.routes[idx]
            stops = route.stops.copy()
            roads = route.roads.copy()

            if west:
                stops.reverse()
                roads.reverse()

            for i, road in enumerate(roads):
                # Passengers leave
                for passenger in reversed(passengers):
                    if np.random.uniform() >= self.q:
                        continue

                    passenger.action.interrupt()
                    passengers.remove(passenger)

                    if self.verbose:
                        print(
                            f"Passenger {passenger.name} left Bus "
                            f"{self.number} at {self.env.now}."
                        )

                if i and self.verbose:
                    print(
                        f"Bus {self.number} arrived at {current_stop}. There "
                        f"are {len(passengers)} passengers in the bus. There "
                        f"are {len(current_stop.items)} passengers waiting at "  # type: ignore
                        f"the stop."
                    )

                # Passengers enter
                while len(passengers) < self.c and i and current_stop.items:  # type: ignore
                    event, passenger = yield current_stop.get()  # type: ignore
                    event.succeed()  # type: ignore
                    passengers.append(passenger)

                    if not self.verbose:
                        continue

                    print(
                        f"Passenger {passenger.name} entered Bus "
                        f"{self.number} at {self.env.now}."
                    )

                n = len(passengers)
                self.bus_utilisation.append(n / self.c)

                if i and self.verbose:
                    print(
                        f"Bus {self.number} left {current_stop}. There "
                        f"are {len(passengers)} passengers in the bus."
                    )

                # Drive to the next stop
                yield self.env.timeout(road)

                current_stop = (
                    stops[i][west]
                    if i < len(stops)
                    else find_end_stop(idx, start_stop)  # type: ignore
                )
