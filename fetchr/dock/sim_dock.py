from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SimDockClient:
    events: list[dict] = field(default_factory=list)

    def push_sample(self) -> dict:
        sample = {'color': 'normal', 'moisture': 0.54, 'weight_g': 32.0}
        self.events.append(sample)
        return sample
