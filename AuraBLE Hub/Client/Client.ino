#include <BLEDevice.h>

void setup() {
  Serial.begin(115200);
  BLEDevice::init("TestClient");
  BLEClient* client = BLEDevice::createClient();
  Serial.println("✅ BLE Client creado correctamente");
}

void loop() {}
