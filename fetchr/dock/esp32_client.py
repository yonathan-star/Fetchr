from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ESP32DockClient:
    endpoint: str
    timeout_s: float = 2.0

    def push_sample(self) -> dict:
        import requests

        payload = {'event': 'request_latest_sample'}
        resp = requests.post(self.endpoint, json=payload, timeout=self.timeout_s)
        resp.raise_for_status()
        return resp.json()
