# Fetchr

Fetchr is a two-part autonomous robotic system:
- **Rover**: follows owner, detects/collects dog waste.
- **Smart dock**: charges rover and analyzes collected samples.

## What this code currently does

### Runtime flow
The runtime is an explicit state machine with these states:
1. `FOLLOW_OWNER` — drives toward owner using phone-position or RSSI follower.
2. `WASTE_SCAN` — queries a **single-camera** pipeline for waste detection.
3. `APPROACH_TARGET` — slow straight approach for pickup.
4. `COLLECT_SEQUENCE` — runs scoop arm collect cycle.
5. `RETURN_TO_DOCK` — placeholder handoff to docking logic.
6. `DOCKED_ANALYZE` — requests sample data from dock endpoint (only when `--dock-enabled`).
7. `FAULT` — safe stop on collection failure.

### Owner tracking options
- `--follower phone` (default): UDP phone position tracking input.
- `--follower rssi`: BLE RSSI-based fallback.

### Single camera + LED options
- `--camera esp32cam`: uses ESP32-CAM stream URL + side LED wrapper (2 regular LEDs, 1 control pin).
- `--camera huskylens`: uses HuskyLens serial adapter + side LED wrapper.
- `--camera yolo`: local YOLO stub.

### Simulation mode
`--sim` runs the full state machine with no hardware using simulated components.

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

### Real hardware (phone-tracking + ESP32-CAM + side LED, dock disabled by default)
```bash
python -m fetchr.scripts.run_rover \
  --port COM11 \
  --follower phone \
  --phone-port 9988 \
  --follow-distance-m 1.5 \
  --camera esp32cam \
  --esp32cam-stream http://192.168.4.1:81/stream \
  --led-gpio 21 \
  --led-count 2 \
  --dock-endpoint http://192.168.4.1/sample
```

### Real hardware (phone-tracking + HuskyLens + side LED)
```bash
python -m fetchr.scripts.run_rover \
  --port COM11 \
  --follower phone \
  --phone-port 9988 \
  --camera huskylens \
  --huskylens-port /dev/ttyUSB1 \
  --led-gpio 21 \
  --led-count 2
```


### Future dock phase
Enable dock analysis only when dock sensors are built:
```bash
python -m fetchr.scripts.run_rover --dock-enabled --dock-endpoint http://192.168.4.1/sample
```

## Phone packet format for motion tracking
Send UDP packets to rover IP on `--phone-port` with JSON:
```json
{"x": 2.4, "y": 0.5}
```
Where `x`,`y` are local meters in rover-start frame.


## Camera-only control (no phone tracking required)
### ESP32 Arduino sketch for HuskyLens + LEDs
Upload this sketch to your ESP32:
- `arduino/fetchr_huskylens_bridge/fetchr_huskylens_bridge.ino`

Wiring + setup notes are in:
- `docs/HUSKYLENS_ESP32_SCRIPT.md`

If you want to skip phone tracking and just use camera detections to steer the robot, use the bridge script:

```bash
python -m fetchr.scripts.bridge_camera_follow   --esp-port COM5   --robot-port COM11   --target-id 1
```

What this does:
- Reads lines like `ID=1 x=156 y=148` from ESP32 serial.
- Turns left/right based on x-position thresholds.
- Drives forward when the object is centered.
- Stops if no detections are received for the timeout window.

## Test
```bash
python -m unittest discover -s tests -v
```

## Hardware still needed for full build
See `docs/BOM_AND_WIRING.md` for complete parts list and wiring instructions.

If you want the no-jargon checklist, read: `docs/WHAT_YOU_NEED_SIMPLE.md`.
