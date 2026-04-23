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
- LEDs are controlled by a photoresistor (LDR) on GPIO34.
- LEDs turn **ON in low light** even if camera detects nothing.
- LEDs turn **OFF in bright light**.
- Tune `LIGHT_THRESHOLD` in the sketch for your environment.
