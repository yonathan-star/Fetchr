from dataclasses import dataclass, field


@dataclass
class DriveConfig:
    follow_speed_mm_s: int = 140
    max_speed_mm_s: int = 220
    turn_gain: float = 1.2
    deadband: float = 0.08


@dataclass
class VisionConfig:
    scan_interval_s: float = 0.25
    detect_threshold: float = 0.55
    lock_threshold: float = 0.72


@dataclass
class CollectConfig:
    pause_before_collect_s: float = 0.4
    settle_after_collect_s: float = 0.6


@dataclass
class FetchrConfig:
    serial_port: str = '/dev/ttyUSB0'
    dock_enabled: bool = False
    drive: DriveConfig = field(default_factory=DriveConfig)
    vision: VisionConfig = field(default_factory=VisionConfig)
    collect: CollectConfig = field(default_factory=CollectConfig)
