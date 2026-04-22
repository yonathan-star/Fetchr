from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Pose2D:
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0


@dataclass
class WasteDetection:
    present: bool
    confidence: float = 0.0
    cx: float = 0.0
    cy: float = 0.0


class BaseDriver(Protocol):
    def start(self) -> None: ...

    def safe(self) -> None: ...

    def stop(self) -> None: ...

    def drive_direct(self, left_mm_s: int, right_mm_s: int) -> None: ...


class Follower(Protocol):
    def read_distance_proxy(self) -> float: ...

    def read_heading_error(self) -> float: ...


class VisionPipeline(Protocol):
    def infer(self) -> WasteDetection: ...


class LightController(Protocol):
    def set_enabled(self, enabled: bool) -> None: ...


class ScoopArm(Protocol):
    def collect_cycle(self) -> bool: ...


class DockClient(Protocol):
    def push_sample(self) -> dict: ...
