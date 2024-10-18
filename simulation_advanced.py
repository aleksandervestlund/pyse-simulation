from collections.abc import Generator, Sequence

import numpy as np
from simpy import Environment, Timeout

from source.bin import Bin
from source.bus import Bus
from source.passenger import Passenger
from source.route_utils import Metric, create_routes


def passenger_generator(
    env: Environment, stop: Bin, rate: float, passengers: list[Passenger]
) -> Generator[Timeout, None, None]:
    while True:
        yield env.timeout(np.random.exponential(rate ** (-1)))
        passengers.append(Passenger(env, stop))


def run_simulation(
    cap: int,
    q: float,
    bus_utilisation: Sequence[list[float]],
    passengers: list[Passenger],
    metric: Metric,
    *,
    rates: list[float] | None = None,
    verbose: bool = True,
    sim_time: int = 60 * 24,
) -> None:
    env = Environment()
    stops_e = [Bin(env, f"{i}e") for i in range(1, 8)]
    stops_w = [Bin(env, f"{i}w") for i in range(1, 8)]
    roads = [3, 7, 6, 1, 4, 3, 9, 1, 3, 8, 8, 5, 6, 2, 3]
    routes = create_routes(stops_e, stops_w, roads)

    if rates is None:
        rates = [
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
        ]

    for i in range(0, len(rates), 2):
        idx = i // 2
        env.process(
            passenger_generator(env, stops_e[idx], rates[i], passengers)
        )
        env.process(
            passenger_generator(env, stops_w[idx], rates[i + 1], passengers)
        )

    for i, bus_util in enumerate(bus_utilisation):
        Bus(env, cap, i, routes, q, bus_util, metric, verbose)

    env.run(sim_time)

    for passenger in passengers:
        if not passenger.wait_time:
            passenger.wait_time = sim_time - passenger.start_time
        if not passenger.travel_time:
            passenger.travel_time = sim_time - passenger.start_time

    if verbose:
        print()

        for stop_e, stop_w in zip(stops_e, stops_w):
            print(f"Stop {stop_e.name} had {stop_e.total} passengers.")
            print(f"Stop {stop_w.name} had {stop_w.total} passengers.")
