from __future__ import annotations

import re
from dataclasses import dataclass

_LINE_RE = re.compile(r"ID=(\d+)\s+x=(\d+)\s+y=(\d+)")


@dataclass(frozen=True)
class HuskyLensDetection:
    object_id: int
    x: int
    y: int


def parse_detection_line(line: str) -> HuskyLensDetection | None:
    """Parse one HuskyLens serial text line like: 'ID=1 x=156 y=148'."""
    match = _LINE_RE.search(line)
    if not match:
        return None

    return HuskyLensDetection(
        object_id=int(match.group(1)),
        x=int(match.group(2)),
        y=int(match.group(3)),
    )
