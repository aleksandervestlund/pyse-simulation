import random
from collections.abc import Generator, Sequence

import numpy as np
from simpy import Environment, Timeout

from source.bin import Bin
from source.bus import find_end_stop
from source.route import Route
from source.route_utils import create_routes


def passenger_generator(
    env: Environment, stop: Bin, rate: float, verbose: bool
) -> Generator[Timeout, None, None]:
    while True:
        yield env.timeout(np.random.exponential(rate ** (-1)))
        stop.put(env.now)

        if verbose:
            print(f"Passenger arrived at {stop.name} at {env.now}.")


def bus(
    env: Environment,
    c: int,
    number: int,
    routes: Sequence[Route],
    q: float,
    bus_utilisation: list[float],
    verbose: bool,
) -> Generator[Timeout, None, None]:
    current_stop = random.randint(1, 4)
    west = current_stop in {1, 2}
    rest = c
    n = 0
    available_routes = {1: (0, 1), 2: (2, 3), 3: (0, 2), 4: (1, 3)}

    while True:
        west = not west
        idx = random.choice(available_routes[current_stop])

        start_stop = current_stop
        route = routes[idx]
        stops = route.stops.copy()
        roads = route.roads.copy()

        if west:
            stops.reverse()
            roads.reverse()

        for i, road in enumerate(roads):
            m = sum(np.random.random(n) < q)
            pass_avail = len(current_stop.items) if i else 0  # type: ignore

            n -= m
            rest += m

            passengers = min(rest, pass_avail)
            n += passengers
            rest -= passengers

            bus_utilisation.append(n / c)

            if verbose:
                print(f"Bus {number} has {n} passengers at {env.now}.")

            for _ in range(passengers):
                if not (i and current_stop.items):  # type: ignore
                    break

                yield current_stop.get()  # type: ignore

            yield env.timeout(road)

            current_stop = (
                stops[i][west]
                if i < len(stops)
                else find_end_stop(idx, start_stop)  # type: ignore
            )


def run_simulation(
    cap: int,
    q: float,
    bus_utilisation: list[list[float]],
    *,
    verbose: bool = True,
    sim_time: int = 60 * 24,
) -> None:
    env = Environment()
    stops_e = [Bin(env, f"{i}e") for i in range(1, 8)]
    stops_w = [Bin(env, f"{i}w") for i in range(1, 8)]
    roads = (3, 7, 6, 1, 4, 3, 9, 1, 3, 8, 8, 5, 6, 2, 3)
    routes = create_routes(stops_e, stops_w, roads)

    rates = (
        0.3,
        0.6,
        0.1,
        0.1,
        0.3,
        0.9,
        0.2,
        0.5,
        0.6,
        0.4,
        0.6,
        0.4,
        0.6,
        0.4,
    )

    for i in range(0, len(rates), 2):
        idx = i // 2
        env.process(passenger_generator(env, stops_e[idx], rates[i], verbose))
        env.process(
            passenger_generator(env, stops_w[idx], rates[i + 1], verbose)
        )

    for i, bus_util in enumerate(bus_utilisation):
        env.process(bus(env, cap, i, routes, q, bus_util, verbose))

    env.run(sim_time)
