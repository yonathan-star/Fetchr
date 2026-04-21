from __future__ import annotations

import logging
import time

from fetchr.core.config import FetchrConfig
from fetchr.core.controller import FetchrController
from fetchr.dock.esp32_client import ESP32DockClient
from fetchr.drivers.create2_driver import Create2Driver
from fetchr.drivers.servo_arm import ServoArm
from fetchr.follow.rssi_follower import RSSIFollower
from fetchr.vision.pipeline import YoloWastePipeline

logging.basicConfig(level=logging.INFO)


def main() -> None:
    config = FetchrConfig(serial_port='COM11')

    controller = FetchrController(
        config=config,
        base=Create2Driver(port=config.serial_port),
        follower=RSSIFollower(target_addr='AA:BB:CC:DD:EE:FF'),
        vision=YoloWastePipeline(detect_threshold=config.vision.detect_threshold),
        arm=ServoArm(),
        dock=ESP32DockClient(endpoint='http://192.168.4.1/sample'),
    )

    controller.boot()
    try:
        while True:
            controller.tick()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        controller.shutdown()


if __name__ == '__main__':
    main()
