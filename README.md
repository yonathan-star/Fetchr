# Fetchr

Fetchr is a two-part autonomous robotic system:
- **Rover**: follows owner, detects/collects dog waste.
- **Smart dock**: charges rover and analyzes collected samples.

## What this code currently does

### Runtime flow
The runtime is an explicit state machine with these states:
1. `FOLLOW_OWNER` — drives based on BLE follower signals.
2. `WASTE_SCAN` — queries vision pipeline for waste detection.
3. `APPROACH_TARGET` — slow straight approach for pickup.
4. `COLLECT_SEQUENCE` — runs scoop arm collect cycle.
5. `RETURN_TO_DOCK` — placeholder handoff to docking logic.
6. `DOCKED_ANALYZE` — requests sample data from dock endpoint.
7. `FAULT` — safe stop on collection failure.

### Hardware mode
In hardware mode, it composes:
- `Create2Driver` (`pycreate2`) for drive commands,
- `RSSIFollower` stub,
- `YoloWastePipeline` stub,
- `ServoArm` stub,
- `ESP32DockClient` for HTTP sample push.

### Simulation mode
`--sim` runs the full state machine with no hardware using simulated components. This is the fastest way to verify logic before touching the robot.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

### Simulation (recommended first)
```bash
python -m fetchr.scripts.run_rover --sim --ticks 40 --sim-distance 0.01 --sim-waste --sim-confidence 0.99
```

### Real hardware
```bash
python -m fetchr.scripts.run_rover --port COM11 --target-addr AA:BB:CC:DD:EE:FF --dock-endpoint http://192.168.4.1/sample
```

## Test
```bash
python -m unittest discover -s tests -v
```

## Hardware still needed for full build
See `docs/BOM_AND_WIRING.md` for complete parts list and wiring instructions.
