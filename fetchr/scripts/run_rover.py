from __future__ import annotations

import argparse
import logging

from fetchr.core.config import FetchrConfig
from fetchr.core.controller import FetchrController
from fetchr.dock.esp32_client import ESP32DockClient
from fetchr.dock.noop_dock import NoopDockClient
from fetchr.dock.sim_dock import SimDockClient
from fetchr.drivers.create2_driver import Create2Driver
from fetchr.drivers.servo_arm import ServoArm
from fetchr.drivers.simulated import SimBaseDriver, SimScoopArm
from fetchr.follow.phone_position_follower import PhonePositionFollower
from fetchr.follow.rssi_follower import RSSIFollower
from fetchr.follow.sim_follower import SimFollower
from fetchr.vision.pipeline import YoloWastePipeline
from fetchr.vision.sim_pipeline import SimVisionPipeline
from fetchr.vision.single_camera import ESP32CamDetector, FixedLedLight, HuskyLensDetector, LitVisionPipeline

logging.basicConfig(level=logging.INFO)


def _build_follower(args: argparse.Namespace):
    if args.sim:
        return SimFollower(distance_proxy=args.sim_distance, heading_error=args.sim_heading)
    if args.follower == 'phone':
        return PhonePositionFollower(bind_port=args.phone_port, target_follow_distance_m=args.follow_distance_m)
    return RSSIFollower(target_addr=args.target_addr)


def _build_vision(args: argparse.Namespace, config: FetchrConfig):
    if args.sim:
        return SimVisionPipeline(present=args.sim_waste, confidence=args.sim_confidence)

    if args.camera == 'esp32cam':
        detector = ESP32CamDetector(stream_url=args.esp32cam_stream, detect_threshold=config.vision.detect_threshold)
        return LitVisionPipeline(detector=detector, light=FixedLedLight(gpio_pin=args.led_gpio, led_count=args.led_count))

    if args.camera == 'huskylens':
        detector = HuskyLensDetector(serial_port=args.huskylens_port, detect_threshold=config.vision.detect_threshold)
        return LitVisionPipeline(detector=detector, light=FixedLedLight(gpio_pin=args.led_gpio, led_count=args.led_count))

    return YoloWastePipeline(detect_threshold=config.vision.detect_threshold)


def _build_dock(args: argparse.Namespace):
    if args.sim:
        return SimDockClient()
    if args.dock_enabled:
        return ESP32DockClient(endpoint=args.dock_endpoint)
    return NoopDockClient()


def build_controller(args: argparse.Namespace) -> FetchrController:
    config = FetchrConfig(serial_port=args.port, dock_enabled=args.dock_enabled)

    if args.sim:
        base = SimBaseDriver()
        arm = SimScoopArm(should_succeed=not args.sim_collect_fail)
    else:
        base = Create2Driver(port=config.serial_port)
        arm = ServoArm()

    return FetchrController(
        config=config,
        base=base,
        follower=_build_follower(args),
        vision=_build_vision(args, config),
        arm=arm,
        dock=_build_dock(args),
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Run Fetchr rover control loop.')
    p.add_argument('--port', default='/dev/ttyUSB0', help='Create2 serial port, e.g. COM11 or /dev/ttyUSB0')
    p.add_argument('--ticks', type=int, default=None, help='Run fixed number of control ticks then exit')
    p.add_argument('--period', type=float, default=0.05, help='Loop period in seconds')

    p.add_argument('--follower', choices=['rssi', 'phone'], default='phone', help='Owner tracking mode')
    p.add_argument('--target-addr', default='AA:BB:CC:DD:EE:FF', help='Owner BLE target address for RSSI mode')
    p.add_argument('--phone-port', type=int, default=9988, help='UDP port for phone position packets')
    p.add_argument('--follow-distance-m', type=float, default=1.5, help='Desired follow spacing for phone tracking')

    p.add_argument('--camera', choices=['yolo', 'esp32cam', 'huskylens'], default='esp32cam', help='Single camera mode')
    p.add_argument('--esp32cam-stream', default='http://192.168.4.1:81/stream', help='ESP32-CAM stream URL')
    p.add_argument('--huskylens-port', default='/dev/ttyUSB1', help='HuskyLens serial port')
    p.add_argument('--led-gpio', type=int, default=21, help='GPIO pin controlling LED driver')
    p.add_argument('--led-count', type=int, default=2, help='Number of regular LEDs wired to same control pin')

    p.add_argument('--dock-enabled', action='store_true', help='Enable dock sensor analysis phase (future hardware)')
    p.add_argument('--dock-endpoint', default='http://192.168.4.1/sample', help='ESP32 dock API endpoint')

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
