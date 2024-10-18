from collections.abc import Sequence
from enum import StrEnum, auto

import numpy as np
from simpy import Environment

from source.bin import Bin
from source.route import Route


class Metric(StrEnum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> str:
        return name.replace("_", " ").capitalize()

    PASSENGERS_PER_TIME = auto()
    MEAN_WAITING_TIME = auto()
    RANDOM = auto()


def create_routes(
    stops_e: Sequence[Bin], stops_w: Sequence[Bin], roads: Sequence[int]
) -> Sequence[Route]:
    routes: list[Route] = []

    routes.append(
        Route(
            [
                (stops_e[0], stops_w[0]),
                (stops_e[3], stops_w[3]),
                (stops_e[5], stops_w[5]),
            ],
            [roads[0], roads[4], roads[7], roads[12]],
        )
    )
    routes.append(
        Route(
            [
                (stops_e[1], stops_w[1]),
                (stops_e[4], stops_w[4]),
                (stops_e[6], stops_w[6]),
            ],
            [roads[1], roads[6], roads[10], roads[14]],
        )
    )
    routes.append(
        Route(
            [
                (stops_e[1], stops_w[1]),
                (stops_e[4], stops_w[4]),
                (stops_e[5], stops_w[5]),
            ],
            [roads[2], roads[6], roads[8], roads[12]],
        )
    )
    routes.append(
        Route(
            [
                (stops_e[2], stops_w[2]),
                (stops_e[6], stops_w[6]),
            ],
            [roads[3], roads[11], roads[14]],
        )
    )

    return routes


def pick_route(
    start_stop: int,
    routes: Sequence[Route],
    env: Environment,
    metric: Metric,
    west: bool,
) -> int:
    available_routes = {1: (0, 1), 2: (2, 3), 3: (0, 2), 4: (1, 3)}
    idx_1, idx_2 = available_routes[start_stop]

    match metric:
        case Metric.PASSENGERS_PER_TIME:
            choice_1 = routes[idx_1].passengers_per_time(west)
            choice_2 = routes[idx_2].passengers_per_time(west)

            if choice_1 > choice_2:
                return idx_1
            return idx_2
        case Metric.MEAN_WAITING_TIME:
            choice_1 = routes[idx_1].mean_waiting_time(env, west)
            choice_2 = routes[idx_2].mean_waiting_time(env, west)

            if choice_1 > choice_2:
                return idx_1
            return idx_2
        case Metric.RANDOM:
            if round(np.random.uniform()):
                return idx_1
            return idx_2
