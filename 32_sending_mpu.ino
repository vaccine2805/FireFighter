#include <SoftwareSerial.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;
SoftwareSerial HC12(16, 17); // HC-12 module connected to digital pins 16 (TX) and 17 (RX)

void setup() {
  Serial.begin(115200);
  HC12.begin(9600); // Initialize the HC-12 module at a baud rate of 9600
  while (!Serial);
  if (!mpu.begin()) {
    while (1);
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  String data = String(a.acceleration.x)+","+String(a.acceleration.y)+","+String(a.acceleration.z)+"|"+String(g.gyro.x)+","+String(g.gyro.y)+","+String(g.gyro.z);
  Serial.println(data); // Print to the Serial Monitor
  HC12.println(data); // Send data to the HC-12 module
  delay(1);
}
