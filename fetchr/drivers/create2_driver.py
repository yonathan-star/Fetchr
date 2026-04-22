from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Create2Driver:
    port: str
    baud: int = 115200

    def __post_init__(self) -> None:
        from pycreate2 import Create2

        Create2.__del__ = lambda self: None  # Avoid noisy destructor on some platforms.
        self.robot = Create2(self.port, self.baud)

    def start(self) -> None:
        self.robot.start()

    def safe(self) -> None:
        self.robot.safe()

    def stop(self) -> None:
        self.drive_direct(0, 0)

    def drive_direct(self, left_mm_s: int, right_mm_s: int) -> None:
        self.robot.drive_direct(left_mm_s, right_mm_s)

    def close(self) -> None:
        try:
            self.stop()
        finally:
            self.robot.close()
            logger.info('Closed Create 2 serial connection.')
