#include <SoftwareSerial.h>

SoftwareSerial HC12(2, 3); //ประกาศขา HC-12

void setup() {
  Serial.begin(9600); // เริ่มต้นการทำงาน Serial monitor
  HC12.begin(9600); // เริ่มต้นการทำงาน Hc-12
}

void loop() {
  if (HC12.available()) { // ตรวจสอบว่ามีข้อมูลใดๆ พร้อมให้อ่านจากโมดูล HC-12 หรือไม่ module
    String data = HC12.readStringUntil('\n'); // อ่านข้อมูลจากโมดูล HC-12 จนกว่าจะพบตัวอักษรตัวใหม่ (newline character, '\n') เพื่อแปลงข้อมูลที่ได้รับให้เป็นสตริงและกำหนดให้ตัวแปร data 
    Serial.println(data); // Print the data to the serial monitor
  }
}
