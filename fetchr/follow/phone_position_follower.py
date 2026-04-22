from __future__ import annotations

import json
import math
import socket
from dataclasses import dataclass, field


@dataclass
class PhonePositionFollower:
    """Follower that tracks owner from phone position updates.

    Expects UDP packets containing JSON payload:
    {"x": <meters>, "y": <meters>, "heading": <radians_optional>}

    `x` and `y` should be in a local coordinate frame relative to rover start.
    """

    bind_host: str = '0.0.0.0'
    bind_port: int = 9988
    target_follow_distance_m: float = 1.5
    heading_gain: float = 0.8
    _sock: socket.socket = field(init=False, repr=False)
    _target_x: float = 0.0
    _target_y: float = 0.0

    def __post_init__(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self.bind_host, self.bind_port))
        self._sock.setblocking(False)

    def _poll_phone_packet(self) -> None:
        try:
            packet, _ = self._sock.recvfrom(2048)
        except BlockingIOError:
            return

        try:
            payload = json.loads(packet.decode('utf-8'))
            self._target_x = float(payload.get('x', self._target_x))
            self._target_y = float(payload.get('y', self._target_y))
        except (ValueError, TypeError, json.JSONDecodeError):
            return

    def read_distance_proxy(self) -> float:
        self._poll_phone_packet()
        dist = math.sqrt(self._target_x**2 + self._target_y**2)
        # Smaller value means closer to desired follow spacing.
        return abs(dist - self.target_follow_distance_m)

    def read_heading_error(self) -> float:
        self._poll_phone_packet()
        angle = math.atan2(self._target_y, self._target_x) if (self._target_x or self._target_y) else 0.0
        return max(-1.0, min(1.0, angle * self.heading_gain))

    def close(self) -> None:
        self._sock.close()
