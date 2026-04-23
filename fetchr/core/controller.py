from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from fetchr.core.config import FetchrConfig
from fetchr.core.interfaces import BaseDriver, DockClient, Follower, ScoopArm, VisionPipeline
from fetchr.core.states import RoverState

logger = logging.getLogger(__name__)


@dataclass
class FetchrController:
    """Main state-machine orchestration for Fetchr rover+dock workflow."""

    config: FetchrConfig
    base: BaseDriver
    follower: Follower
    vision: VisionPipeline
    arm: ScoopArm
    dock: DockClient
    state: RoverState = RoverState.IDLE

    def boot(self) -> None:
        self.base.start()
        self.base.safe()
        self.state = RoverState.FOLLOW_OWNER
        logger.info('Fetchr boot complete. Entered FOLLOW_OWNER state.')

    def tick(self) -> None:
        if self.state == RoverState.FOLLOW_OWNER:
            self._follow_owner_tick()
            return

        if self.state == RoverState.WASTE_SCAN:
            det = self.vision.infer()
            if det.present and det.confidence >= self.config.vision.lock_threshold:
                self.state = RoverState.APPROACH_TARGET
            else:
                self.state = RoverState.FOLLOW_OWNER
            return

        if self.state == RoverState.APPROACH_TARGET:
            self.base.drive_direct(80, 80)
            time.sleep(0.5)
            self.base.stop()
            self.state = RoverState.COLLECT_SEQUENCE
            return

        if self.state == RoverState.COLLECT_SEQUENCE:
            ok = self.arm.collect_cycle()
            self.state = RoverState.RETURN_TO_DOCK if ok else RoverState.FAULT
            return

        if self.state == RoverState.RETURN_TO_DOCK:
            self.base.stop()
            if self.config.dock_enabled:
                self.state = RoverState.DOCKED_ANALYZE
            else:
                self.state = RoverState.FOLLOW_OWNER
            return

        if self.state == RoverState.DOCKED_ANALYZE:
            data = self.dock.push_sample()
            logger.info('Dock analysis payload: %s', data)
            self.state = RoverState.FOLLOW_OWNER
            return

        if self.state == RoverState.FAULT:
            self.base.stop()

    def _follow_owner_tick(self) -> None:
        distance_proxy = self.follower.read_distance_proxy()
        heading_error = self.follower.read_heading_error()

        if distance_proxy <= self.config.drive.deadband:
            self.base.stop()
            self.state = RoverState.WASTE_SCAN
            return

        turn = int(self.config.drive.turn_gain * heading_error * 100)
        base_speed = self.config.drive.follow_speed_mm_s
        max_speed = self.config.drive.max_speed_mm_s

        left = max(-max_speed, min(max_speed, base_speed - turn))
        right = max(-max_speed, min(max_speed, base_speed + turn))
        self.base.drive_direct(left, right)

    def run_loop(self, ticks: int | None = None, period_s: float = 0.05) -> None:
        """Run control loop forever (ticks=None) or for a fixed number of ticks."""
        i = 0
        while ticks is None or i < ticks:
            self.tick()
            i += 1
            time.sleep(period_s)

    def shutdown(self) -> None:
        self.base.stop()
        base_close = getattr(self.base, 'close', None)
        if callable(base_close):
            base_close()

        follower_close = getattr(self.follower, 'close', None)
        if callable(follower_close):
            follower_close()
