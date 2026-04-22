# Fetchr: What you need (super simple)

## I am picking for you: **ESP32-CAM**
Why: you need poop detection, and ESP32-CAM gives you a real image stream that can later be improved with better models.

---

## You already have
- iRobot Create 2
- Raspberry Pi 4 (assuming from your plan)
- ESP32 board
- ESP32-CAM or HuskyLens (we are choosing **ESP32-CAM**)

---

## Buy/bring this extra stuff

### Required to make rover move + scoop
1. USB-to-Mini-DIN Create 2 serial cable (7-pin DIN to USB)
2. 2x metal gear servos (for scoop arm)
3. PCA9685 servo driver board
4. External 5V 3A power rail for servos (buck converter + wiring)
5. Emergency stop button (latching)
6. Mounting hardware (brackets, screws, standoffs)
7. Waste bin + liner + lid/seal

### Required for camera + light
8. ESP32-CAM module (if not already this exact module)
9. Side LED light (white LED module) + transistor/resistor driver
10. Stable 5V supply for camera/light

### Required for dock health sensing
11. TCS34725 color sensor
12. HX711 + load cell
13. Capacitive moisture probe
14. Wires, breadboard/perfboard, connectors

### Nice-to-have but strongly recommended
15. Inline fuse for servo power rail
16. Limit switches (2) for scoop arm end stops
17. Waterproof enclosure bits / splash guards

---

## How it connects (simple)
1. **Create 2 -> Pi:** serial cable from Create 2 DIN port to Pi USB.
2. **Phone -> Pi:** phone app sends UDP packets with position to Pi on port 9988.
3. **ESP32-CAM -> Pi:** same Wi-Fi network; Pi pulls stream URL.
4. **LED -> Pi GPIO21:** GPIO controls LED driver transistor.
5. **Servos -> PCA9685:** PCA9685 controlled over Pi I2C (SDA/SCL), servos powered by external 5V rail.
6. **Dock sensors -> ESP32:** TCS34725 (I2C), HX711/load cell, moisture probe to ADC.

---

## Minimum first test plan
1. Test Create 2 movement only.
2. Test phone position packet input only.
3. Test ESP32-CAM stream + LED toggle only.
4. Test servo arm movement only.
5. Run full software in `--sim` first, then hardware mode.

---

## One command to start in simulation
```bash
python -m fetchr.scripts.run_rover --sim --ticks 40 --sim-distance 0.01 --sim-waste --sim-confidence 0.99
```

## One command to start in hardware (ESP32-CAM path)
```bash
python -m fetchr.scripts.run_rover \
  --port COM11 \
  --follower phone \
  --phone-port 9988 \
  --camera esp32cam \
  --esp32cam-stream http://192.168.4.1:81/stream \
  --led-gpio 21
```
