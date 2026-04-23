from __future__ import annotations

from dataclasses import dataclass

from fetchr.core.interfaces import WasteDetection


@dataclass
class SimVisionPipeline:
    present: bool = False
    confidence: float = 0.0

    def infer(self) -> WasteDetection:
        return WasteDetection(present=self.present, confidence=self.confidence, cx=0.5, cy=0.5)
