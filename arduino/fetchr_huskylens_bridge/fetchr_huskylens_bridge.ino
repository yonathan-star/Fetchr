#include "HUSKYLENS.h"

// Fetchr ESP32 -> HuskyLens UART bridge + dual LED illumination
// - Reads detections from HuskyLens over UART2
// - Uses camera output (no external photoresistor) to decide when to turn lights on
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

// Camera-only low-light heuristic:
// if HuskyLens reports no detections for this many frames, treat as "low-light"
// and enable scene LEDs. Tune this value for your environment.
constexpr int LOW_LIGHT_NO_DETECTION_FRAMES = 8;
int noDetectionFrames = 0;

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
    Serial.println("request FAIL");
    delay(120);
    return;
  }

  int availableCount = huskylens.available();
  bool hasDetections = availableCount > 0;

  if (hasDetections) {
    noDetectionFrames = 0;
  } else {
    noDetectionFrames++;
  }

  bool lowLight = noDetectionFrames >= LOW_LIGHT_NO_DETECTION_FRAMES;
  setLeds(lowLight);

  if (!hasDetections) {
    Serial.print("available: 0 light=");
    Serial.println(lowLight ? "LOW" : "BRIGHT");
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
