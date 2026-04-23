import unittest

from fetchr.core.config import FetchrConfig
from fetchr.core.controller import FetchrController
from fetchr.core.states import RoverState
from fetchr.dock.sim_dock import SimDockClient
from fetchr.drivers.simulated import SimBaseDriver, SimScoopArm
from fetchr.follow.sim_follower import SimFollower
from fetchr.vision.sim_pipeline import SimVisionPipeline


class ControllerTests(unittest.TestCase):
    def _build(self, *, distance=1.0, present=False, confidence=0.0, collect_ok=True):
        return FetchrController(
            config=FetchrConfig(),
            base=SimBaseDriver(),
            follower=SimFollower(distance_proxy=distance, heading_error=0.0),
            vision=SimVisionPipeline(present=present, confidence=confidence),
            arm=SimScoopArm(should_succeed=collect_ok),
            dock=SimDockClient(),
        )

    def test_boot_enters_follow(self):
        c = self._build()
        c.boot()
        self.assertEqual(c.state, RoverState.FOLLOW_OWNER)

    def test_follow_transitions_to_scan_when_close(self):
        c = self._build(distance=0.01)
        c.boot()
        c.tick()
        self.assertEqual(c.state, RoverState.WASTE_SCAN)

    def test_scan_goes_to_approach_when_detection_confident(self):
        c = self._build(distance=0.01, present=True, confidence=0.99)
        c.boot()
        c.tick()  # follow -> scan
        c.tick()  # scan -> approach
        self.assertEqual(c.state, RoverState.APPROACH_TARGET)


    def test_return_to_dock_skips_analysis_when_disabled(self):
        c = self._build(distance=0.01, present=True, confidence=0.99, collect_ok=True)
        c.config.dock_enabled = False
        c.boot()
        c.tick()  # follow -> scan
        c.tick()  # scan -> approach
        c.tick()  # approach -> collect
        c.tick()  # collect -> return_to_dock
        c.tick()  # return_to_dock -> follow_owner (skip dock)
        self.assertEqual(c.state, RoverState.FOLLOW_OWNER)

    def test_collection_failure_goes_fault(self):
        c = self._build(distance=0.01, present=True, confidence=0.99, collect_ok=False)
        c.boot()
        c.tick()  # follow -> scan
        c.tick()  # scan -> approach
        c.tick()  # approach -> collect
        c.tick()  # collect -> fault
        self.assertEqual(c.state, RoverState.FAULT)


if __name__ == '__main__':
    unittest.main()
