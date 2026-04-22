# Fetchr BOM + Wiring Guide

## 1) Additional hardware to bring

### Rover side
- Raspberry Pi 4 (4GB+), 32GB+ microSD, official 5V/3A regulator from robot battery or dedicated buck converter.
- USB-to-Mini-DIN 7 pin serial cable for Create 2 OI.
- **One vision device only** (choose one):
  - ESP32-CAM module, OR
  - HuskyLens AI camera.
- 2x regular white LEDs (side-mounted) controlled from one pin via transistor/driver + resistors.
- 2x high-torque metal gear servos (arm + scoop axis).
- PCA9685 servo driver board (recommended; stable PWM vs direct GPIO).
- Separate 5V 3A rail for servos (do **not** power servos from Pi 5V pin directly).
- PETG waste bin + silicone gasket + removable liner.
- Limit switches (2) for arm end-stop homing.
- Emergency stop latching button that cuts motor/servo power path.

### Dock side (future phase)
- ESP32 dev board.
- TCS34725 color sensor (I2C).
- HX711 amplifier + load cell.
- (Later add-on) Capacitive moisture probe + ADC.
- Enclosed sample tray with repeatable placement geometry.

## 2) Electrical connections

## Rover wiring

### Create 2 <-> Raspberry Pi
- Create 2 OI Mini-DIN via USB serial cable into Pi USB.
- OI serial settings: **115200 baud**, 8N1.

### Phone position tracking
- Rover and phone must be on the same network (or hotspot).
- Phone app sends UDP position packets to Pi IP on port `9988`.

### Single camera option A: ESP32-CAM
- ESP32-CAM powered at stable 5V.
- ESP32-CAM publishes MJPEG stream (default `http://<ip>:81/stream`).
- Pi reads stream over Wi-Fi.

### Single camera option B: HuskyLens
- HuskyLens TX -> Pi RX (UART adapter level-safe) or USB-UART.
- HuskyLens RX -> Pi TX.
- Power/GND per module requirements.

### Side LED illumination
- Pi GPIO21 -> transistor gate/base -> 2 LED branch (single control pin).
- LEDs on separate power rail if current is high.
- Common ground between Pi and LED driver power source.

### Servo subsystem (recommended)
- Pi I2C:
  - Pi `GPIO2/SDA` -> PCA9685 SDA
  - Pi `GPIO3/SCL` -> PCA9685 SCL
  - Pi GND -> PCA9685 GND
- Servo power:
  - External 5V rail -> PCA9685 V+
  - External GND -> PCA9685 GND
  - **Common ground required** between Pi and servo PSU.
- Servos:
  - Servo 1 signal -> PCA9685 CH0
  - Servo 2 signal -> PCA9685 CH1
- End-stops:
  - Limit switch 1 -> Pi GPIO23 with pull-up
  - Limit switch 2 -> Pi GPIO24 with pull-up

### Emergency stop
- Put E-stop inline with servo 5V rail and rover motion enable logic.
- In software, E-stop GPIO immediately commands `drive_direct(0,0)`.

## Dock wiring

### ESP32 I2C
- ESP32 SDA (GPIO21 typical) -> TCS34725 SDA
- ESP32 SCL (GPIO22 typical) -> TCS34725 SCL
- 3V3 and GND shared.

### HX711
- HX711 DT -> ESP32 GPIO18 (example)
- HX711 SCK -> ESP32 GPIO19 (example)
- VCC/GND per module spec.

### Moisture probe
- Probe analog out -> ESP32 ADC pin (e.g., GPIO34 input-only)
- VCC/GND per probe spec.

## 3) Communications
- Rover app stack on Pi:
  - Create 2 control over serial.
  - Phone position tracking over UDP.
  - Single-camera inference + LED assist.
- Dock app stack on ESP32:
  - Sensor acquisition + filtering.
  - WiFi push to phone API endpoint or MQTT topic.

## 4) Bring-up sequence
1. Validate Create 2 drive script only.
   - You can skip dock sensor steps until Phase 2.
2. Validate phone UDP packets are received on Pi.
3. Validate single camera stream/device feed + LED toggle.
4. Validate servo sweep with external PSU.
5. Integrate state machine with simulated components.
6. Replace sim follower/vision with live phone+camera modules.
7. Validate dock color + weight sensors independently.
8. Validate dock-to-phone packet delivery.
9. Add moisture sensor as later extension.
10. Run full end-to-end test with kill switch accessible.

## 5) Safety and reliability checklist
- Never run servos from Pi 5V pin alone.
- Add fuse/current limit on servo rail.
- Keep all grounds common where signals cross boards.
- Add timeout watchdog that stops rover if loop stalls >250 ms.
- Keep first tests at low speed and open area.
