from typing import Any

from simpy import Environment, Store
from simpy.resources.store import StorePut


class Bin(Store):
    def __init__(self, env: Environment, name: str) -> None:
        super().__init__(env)
        self.name = name
        self.total = 0

    def put(self, item: Any) -> StorePut:  # type: ignore
        self.total += 1
        return super().put(item)

    def __repr__(self) -> str:
        return f"Stop {self.name}"
