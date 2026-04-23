#include "HUSKYLENS.h"

// Fetchr ESP32 -> HuskyLens UART bridge + dual LED illumination
// - Reads detections from HuskyLens over UART2
// - Turns on two LEDs when detections are available
// - Prints easy-to-parse lines for the PC bridge script:
//     ID=<id> x=<xCenter> y=<yCenter>

HUSKYLENS huskylens;
HardwareSerial Husky(2);  // UART2 on ESP32

// UART pins between ESP32 and HuskyLens (crossed):
// HuskyLens T -> ESP32 RX2 (GPIO16)
// HuskyLens R -> ESP32 TX2 (GPIO17)
constexpr int HUSKY_RX2_PIN = 16;
constexpr int HUSKY_TX2_PIN = 17;
constexpr int HUSKY_BAUD = 9600;

// Two regular LEDs on separate pins
constexpr int LED1_PIN = 22;
constexpr int LED2_PIN = 23;

// Serial to PC (USB)
constexpr int USB_BAUD = 115200;

void setLeds(bool on) {
  digitalWrite(LED1_PIN, on ? HIGH : LOW);
  digitalWrite(LED2_PIN, on ? HIGH : LOW);
}

void setup() {
  Serial.begin(USB_BAUD);

  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  setLeds(false);

  Husky.begin(HUSKY_BAUD, SERIAL_8N1, HUSKY_RX2_PIN, HUSKY_TX2_PIN);

  if (!huskylens.begin(Husky)) {
    Serial.println("HUSKYLENS begin: FAIL");
    while (true) {
      setLeds(false);
      delay(250);
      setLeds(true);
      delay(250);
    }
  }

  Serial.println("HUSKYLENS begin: OK");
}

void loop() {
  // Request current detections from HuskyLens.
  if (!huskylens.request()) {
    setLeds(false);
    Serial.println("request FAIL");
    delay(120);
    return;
  }

  int availableCount = huskylens.available();
  bool hasDetections = availableCount > 0;
  setLeds(hasDetections);

  if (!hasDetections) {
    Serial.println("available: 0");
    delay(80);
    return;
  }

  // Emit one parseable line per detection.
  while (huskylens.available()) {
    HUSKYLENSResult r = huskylens.read();
    Serial.print("ID=");
    Serial.print(r.ID);
    Serial.print(" x=");
    Serial.print(r.xCenter);
    Serial.print(" y=");
    Serial.println(r.yCenter);
  }

  delay(40);
}
