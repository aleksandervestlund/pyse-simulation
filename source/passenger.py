import os
import random
from collections.abc import Generator
from dataclasses import dataclass, field
from pathlib import Path
from string import ascii_uppercase

from simpy import Environment, Event, Interrupt, Process, Timeout

from source.bin import Bin


def generate_name_list() -> list[str]:
    filepath = os.path.join(Path(__file__).parent.resolve(), "names.txt")

    with open(filepath, encoding="utf-8") as file:
        return file.read().splitlines()


FIRST_NAMES = generate_name_list()
LAST_NAMES = f"{ascii_uppercase}ÆØÅ"


@dataclass(slots=True)
class Passenger:
    env: Environment
    stop: Bin
    name: str = field(init=False)
    action: Process = field(init=False)
    start_time: float = field(init=False)
    wait_time: float = field(default=0.0, init=False)
    travel_time: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        self.start_time = self.env.now
        self.action = self.env.process(self.travel())
        self.name = (
            f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}."
        )

    def travel(self) -> Generator[Event | Timeout, None, None]:
        enter_event = self.env.event()
        self.stop.put((enter_event, self))

        yield enter_event

        self.wait_time = self.env.now - self.start_time

        try:
            yield self.env.timeout(float("inf"))
        except Interrupt:
            self.travel_time = self.env.now - self.start_time
