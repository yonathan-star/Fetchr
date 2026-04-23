from __future__ import annotations

from dataclasses import dataclass
from random import uniform


@dataclass
class RSSIFollower:
    target_addr: str

    def read_distance_proxy(self) -> float:
        # TODO: replace with real BLE scanner; lower is "closer"
        return uniform(0.2, 1.4)

    def read_heading_error(self) -> float:
        # TODO: replace with multi-antenna or movement-based estimation
        return uniform(-0.3, 0.3)
