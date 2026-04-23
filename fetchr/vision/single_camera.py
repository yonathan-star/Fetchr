from __future__ import annotations

from dataclasses import dataclass

from fetchr.core.interfaces import LightController, WasteDetection


@dataclass
class FixedLedLight:
    """Simple LED controller stub for side illumination (2 LEDs on one control pin)."""

    gpio_pin: int = 21
    led_count: int = 2
    enabled: bool = True

    def set_enabled(self, enabled: bool) -> None:
        # TODO: replace with GPIO output call on Pi/MCU.
        self.enabled = enabled


@dataclass
class ESP32CamDetector:
    stream_url: str
    detect_threshold: float = 0.6

    def infer(self) -> WasteDetection:
        # TODO: pull latest frame from ESP32-CAM stream and run inference.
        return WasteDetection(present=False, confidence=0.0, cx=0.5, cy=0.5)


@dataclass
class HuskyLensDetector:
    serial_port: str
    detect_threshold: float = 0.6

    def infer(self) -> WasteDetection:
        # TODO: parse HuskyLens learned object bounding box + confidence.
        return WasteDetection(present=False, confidence=0.0, cx=0.5, cy=0.5)


@dataclass
class LitVisionPipeline:
    detector: object
    light: LightController

    def infer(self) -> WasteDetection:
        self.light.set_enabled(True)
        return self.detector.infer()
