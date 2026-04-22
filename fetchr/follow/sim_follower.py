from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimFollower:
    distance_proxy: float = 1.0
    heading_error: float = 0.0

    def read_distance_proxy(self) -> float:
        return self.distance_proxy

    def read_heading_error(self) -> float:
        return self.heading_error
