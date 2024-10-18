from dataclasses import dataclass

import numpy as np
from numpy import floating
from simpy import Environment

from source.bin import Bin


@dataclass(slots=True, frozen=True)
class Route:
    stops: list[tuple[Bin, Bin]]
    roads: list[int]

    def passengers_per_time(self, west: bool) -> floating:
        return sum(len(stop[west].items) for stop in self.stops) / np.log(
            sum(self.roads)
        )

    def mean_waiting_time(self, env: Environment, west: bool) -> floating:
        waiting_times: list[float] = []

        for stop in self.stops:
            for _, passenger in stop[west].items:
                waiting_times.append(env.now - passenger.start_time)

        return np.mean(waiting_times)
