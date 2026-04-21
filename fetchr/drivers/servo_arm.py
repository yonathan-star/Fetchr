from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class ServoArm:
    extend_gpio: int = 18
    tilt_gpio: int = 19

    def collect_cycle(self) -> bool:
        # TODO: replace with pigpio/RPi.GPIO PWM implementation.
        time.sleep(0.2)  # extend
        time.sleep(0.25)  # scoop
        time.sleep(0.2)  # retract
        return True
