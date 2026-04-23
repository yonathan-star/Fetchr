# HuskyLens + ESP32 script (for Fetchr camera bridge)

Use this sketch file:

- `arduino/fetchr_huskylens_bridge/fetchr_huskylens_bridge.ino`

## Wiring
- HuskyLens `T` -> ESP32 `GPIO16` (RX2)
- HuskyLens `R` -> ESP32 `GPIO17` (TX2)
- HuskyLens `VCC` -> ESP32 `5V`
- HuskyLens `GND` -> ESP32 `GND`
- LED1 anode -> GPIO22 through resistor, cathode -> GND
- LED2 anode -> GPIO23 through resistor, cathode -> GND

## Device settings
On HuskyLens, set protocol to **UART/Serial 9600**.

## Output format (to USB serial monitor)
The sketch emits lines like:

- `ID=1 x=156 y=148`

That format is what `python -m fetchr.scripts.bridge_camera_follow` parses.


## Low-light LED behavior
- LEDs are controlled from HuskyLens camera output only (no photoresistor).
- The sketch treats repeated no-detection frames as low-light and turns LEDs ON.
- The sketch turns LEDs OFF after detections resume.
- Tune `LOW_LIGHT_NO_DETECTION_FRAMES` in the sketch for sensitivity.
