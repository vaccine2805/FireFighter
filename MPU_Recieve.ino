#include <SoftwareSerial.h>

SoftwareSerial HC12(10, 11); // HC-12 module connected to digital pins 10 (RX) and 11 (TX)

void setup() {
  Serial.begin(9600); // Initialize the serial monitor at a baud rate of 9600
  HC12.begin(9600); // Initialize the HC-12 module at a baud rate of 9600
}

void loop() {
  if (HC12.available()) { // If data is available on the HC-12 module
    String data = HC12.readStringUntil('\n'); // Read the data until a new line character is received
    Serial.println(data); // Print the data to the serial monitor
  }
}
