from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SimBaseDriver:
    started: bool = False
    safe_mode: bool = False
    last_left: int = 0
    last_right: int = 0
    command_log: list[tuple[int, int]] = field(default_factory=list)

    def start(self) -> None:
        self.started = True

    def safe(self) -> None:
        self.safe_mode = True

    def stop(self) -> None:
        self.drive_direct(0, 0)

    def drive_direct(self, left_mm_s: int, right_mm_s: int) -> None:
        self.last_left = left_mm_s
        self.last_right = right_mm_s
        self.command_log.append((left_mm_s, right_mm_s))


@dataclass
class SimScoopArm:
    should_succeed: bool = True
    cycles: int = 0

    def collect_cycle(self) -> bool:
        self.cycles += 1
        return self.should_succeed
