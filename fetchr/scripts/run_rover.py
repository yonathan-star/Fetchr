from __future__ import annotations

import argparse
import logging

from fetchr.core.config import FetchrConfig
from fetchr.core.controller import FetchrController
from fetchr.dock.esp32_client import ESP32DockClient
from fetchr.dock.sim_dock import SimDockClient
from fetchr.drivers.create2_driver import Create2Driver
from fetchr.drivers.servo_arm import ServoArm
from fetchr.drivers.simulated import SimBaseDriver, SimScoopArm
from fetchr.follow.rssi_follower import RSSIFollower
from fetchr.follow.sim_follower import SimFollower
from fetchr.vision.pipeline import YoloWastePipeline
from fetchr.vision.sim_pipeline import SimVisionPipeline

logging.basicConfig(level=logging.INFO)


def build_controller(args: argparse.Namespace) -> FetchrController:
    config = FetchrConfig(serial_port=args.port)

    if args.sim:
        return FetchrController(
            config=config,
            base=SimBaseDriver(),
            follower=SimFollower(distance_proxy=args.sim_distance, heading_error=args.sim_heading),
            vision=SimVisionPipeline(present=args.sim_waste, confidence=args.sim_confidence),
            arm=SimScoopArm(should_succeed=not args.sim_collect_fail),
            dock=SimDockClient(),
        )

    return FetchrController(
        config=config,
        base=Create2Driver(port=config.serial_port),
        follower=RSSIFollower(target_addr=args.target_addr),
        vision=YoloWastePipeline(detect_threshold=config.vision.detect_threshold),
        arm=ServoArm(),
        dock=ESP32DockClient(endpoint=args.dock_endpoint),
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Run Fetchr rover control loop.')
    p.add_argument('--port', default='/dev/ttyUSB0', help='Create2 serial port, e.g. COM11 or /dev/ttyUSB0')
    p.add_argument('--target-addr', default='AA:BB:CC:DD:EE:FF', help='Owner BLE target address')
    p.add_argument('--dock-endpoint', default='http://192.168.4.1/sample', help='ESP32 dock API endpoint')
    p.add_argument('--ticks', type=int, default=None, help='Run fixed number of control ticks then exit')
    p.add_argument('--period', type=float, default=0.05, help='Loop period in seconds')

    p.add_argument('--sim', action='store_true', help='Run without hardware using simulation components')
    p.add_argument('--sim-distance', type=float, default=1.0, help='Simulated owner distance proxy')
    p.add_argument('--sim-heading', type=float, default=0.0, help='Simulated heading error')
    p.add_argument('--sim-waste', action='store_true', help='Simulate waste detection as present')
    p.add_argument('--sim-confidence', type=float, default=0.95, help='Simulated detection confidence')
    p.add_argument('--sim-collect-fail', action='store_true', help='Simulate failed collection cycle')
    return p.parse_args()


def main() -> None:
    args = parse_args()
    controller = build_controller(args)
    controller.boot()
    try:
        controller.run_loop(ticks=args.ticks, period_s=args.period)
    except KeyboardInterrupt:
        pass
    finally:
        controller.shutdown()


if __name__ == '__main__':
    main()
