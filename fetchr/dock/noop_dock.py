from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NoopDockClient:
    """Dock placeholder used when dock sensors are deferred to a future phase."""

    def push_sample(self) -> dict:
        return {'status': 'dock_disabled', 'detail': 'Dock sensors planned for future phase.'}
