# Fetchr: What you need (super simple)

## I am picking for you: **ESP32-CAM**
Why: you need poop detection, and ESP32-CAM gives a real video stream you can improve later.

## Your setup decision (based on what you said)
- Put the **ESP32 (or ESP32-CAM)** on the iRobot rover body.
- Wire two regular side LEDs through rover power/electronics using one control pin + proper transistor driver.
- Treat dock sensors as **Phase 2 / future**, not required for first working rover.

---

## You already have
- iRobot Create 2
- ESP32 board
- ESP32-CAM or HuskyLens (we are choosing **ESP32-CAM**)

---

## What else you still need

### Required to make rover move + scoop (Phase 1)
1. Raspberry Pi 4 (main compute) + microSD + 5V/3A supply
2. USB-to-Mini-DIN Create 2 serial cable (7-pin DIN to USB)
3. 2x metal gear servos (for scoop arm)
4. PCA9685 servo driver board
5. External 5V 3A power rail for servos (buck converter + wiring)
6. Emergency stop button (latching)
7. Mounting hardware (brackets, screws, standoffs)
8. Waste bin + liner + lid/seal

### Required for camera + light (Phase 1)
9. ESP32-CAM module (if not already this exact module)
10. 2x regular white LEDs + transistor/resistor driver (one GPIO control pin)
11. Stable 5V supply for camera/light

### Dock sensors (future)
12. TCS34725 color sensor
13. HX711 + load cell
14. Wires, perfboard/connectors

### Moisture sensor (later future add-on)
15. Capacitive moisture probe

---

## How to connect it (simple)
1. **Create 2 -> Pi:** serial cable from Create 2 DIN port to Pi USB.
2. **Phone -> Pi:** phone app sends UDP packets with position to Pi on port 9988.
3. **ESP32-CAM on rover -> Pi:** same Wi-Fi network; Pi reads `http://<esp32cam-ip>:81/stream`.
4. **2 LEDs on rover -> 1 GPIO driver:** one GPIO controls a transistor that powers both LEDs.
5. **Servos -> PCA9685:** PCA9685 over Pi I2C (SDA/SCL), servos on separate 5V rail.
6. **Dock sensors later:** not needed for first rover demo.

---

## First milestone (what “done” means now)
- Rover follows phone position.
- Rover detects/targets poop with ESP32-CAM + LED assist.
- Rover actuates scoop arm.
- Dock analysis can be turned off for now.

---

## Commands
### Simulation first
```bash
python -m fetchr.scripts.run_rover --sim --ticks 40 --sim-distance 0.01 --sim-waste --sim-confidence 0.99
```

### Hardware now (dock disabled by default)
```bash
python -m fetchr.scripts.run_rover \
  --port COM11 \
  --follower phone \
  --phone-port 9988 \
  --camera esp32cam \
  --esp32cam-stream http://192.168.4.1:81/stream \
  --led-gpio 21 \
  --led-count 2
```

### Future when dock sensors are built
```bash
python -m fetchr.scripts.run_rover --dock-enabled --dock-endpoint http://192.168.4.1/sample
```
