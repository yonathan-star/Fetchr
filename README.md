# Fetchr

Fetchr is a two-part autonomous robotic system:
- **Rover**: follows owner, detects/collects dog waste.
- **Smart dock**: charges rover and analyzes collected samples.

## What is included in this scaffold
- State-machine controller for rover mission flow.
- Create 2 driver wrapper (`pycreate2`).
- BLE RSSI follower stub.
- YOLO pipeline stub.
- Servo arm control stub.
- ESP32 dock HTTP client.

## Quick start (development)
1. Create virtual env and install dependencies.
2. Edit `fetchr/scripts/run_rover.py` for your serial port and endpoints.
3. Run:

```bash
python -m fetchr.scripts.run_rover
```

## Hardware still needed for full build
See `docs/BOM_AND_WIRING.md` for complete parts list and wiring instructions.
