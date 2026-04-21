from __future__ import annotations

from dataclasses import dataclass
from random import random

from fetchr.core.interfaces import WasteDetection


@dataclass
class YoloWastePipeline:
    detect_threshold: float = 0.55

    def infer(self) -> WasteDetection:
        conf = random()
        return WasteDetection(
            present=conf >= self.detect_threshold,
            confidence=conf,
            cx=0.5,
            cy=0.5,
        )
