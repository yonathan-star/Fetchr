from __future__ import annotations

import argparse
import time

import serial
from pycreate2 import Create2

from fetchr.vision.huskylens_stream import parse_detection_line


# Avoid noisy pycreate2 shutdown traceback on Windows when port is already closed.
Create2.__del__ = lambda self: None  # type: ignore[attr-defined]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Bridge HuskyLens serial detections from ESP32 to Create2 wheel commands.'
    )
    parser.add_argument('--esp-port', default='COM5', help='ESP32 USB serial port')
    parser.add_argument('--esp-baud', type=int, default=115200, help='ESP32 serial baud')
    parser.add_argument('--robot-port', default='COM11', help='Create2 serial port')
    parser.add_argument('--robot-baud', type=int, default=115200, help='Create2 serial baud')
    parser.add_argument('--left-threshold', type=int, default=130, help='x below this turns left')
    parser.add_argument('--right-threshold', type=int, default=190, help='x above this turns right')
    parser.add_argument('--forward-left', type=int, default=120, help='left wheel speed for forward')
    parser.add_argument('--forward-right', type=int, default=120, help='right wheel speed for forward')
    parser.add_argument('--turn-left-left', type=int, default=70, help='left wheel speed when turning left')
    parser.add_argument('--turn-left-right', type=int, default=130, help='right wheel speed when turning left')
    parser.add_argument('--turn-right-left', type=int, default=130, help='left wheel speed when turning right')
    parser.add_argument('--turn-right-right', type=int, default=70, help='right wheel speed when turning right')
    parser.add_argument('--target-id', type=int, default=None, help='optional learned ID filter (e.g. 1)')
    parser.add_argument('--no-detection-timeout', type=float, default=1.0, help='seconds before stop if no detections')
    parser.add_argument('--loop-delay', type=float, default=0.03, help='loop sleep delay in seconds')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    esp = serial.Serial(args.esp_port, args.esp_baud, timeout=0.2)
    bot = Create2(args.robot_port, args.robot_baud)
    bot.start()
    bot.safe()

    last_seen = time.time()
    print('Bridge running. Ctrl+C to stop.')

    try:
        while True:
            raw = esp.readline().decode(errors='ignore').strip()
            if raw:
                det = parse_detection_line(raw)
                if det:
                    if args.target_id is not None and det.object_id != args.target_id:
                        continue

                    last_seen = time.time()

                    if det.x < args.left_threshold:
                        bot.drive_direct(args.turn_left_left, args.turn_left_right)
                        print(f'LEFT  x={det.x} id={det.object_id}')
                    elif det.x > args.right_threshold:
                        bot.drive_direct(args.turn_right_left, args.turn_right_right)
                        print(f'RIGHT x={det.x} id={det.object_id}')
                    else:
                        bot.drive_direct(args.forward_left, args.forward_right)
                        print(f'FWD   x={det.x} id={det.object_id}')

            if time.time() - last_seen > args.no_detection_timeout:
                bot.drive_direct(0, 0)

            time.sleep(args.loop_delay)

    except KeyboardInterrupt:
        pass
    finally:
        try:
            bot.drive_direct(0, 0)
        except Exception:
            pass
        try:
            bot.close()
        except Exception:
            pass
        esp.close()
        print('Stopped.')


if __name__ == '__main__':
    main()
