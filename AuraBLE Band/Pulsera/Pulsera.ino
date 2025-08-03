#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

// UUIDs personalizados (puedes cambiarlos)
#define SERVICE_UUID        "12345678-1234-5678-1234-56789abcdef0"
#define CHARACTERISTIC_UUID "12345678-1234-5678-1234-56789abcdef1"

BLECharacteristic *pCharacteristic;

void setup() {
  Serial.begin(115200);
  Serial.println("🔧 Iniciando BLE...");

  BLEDevice::init("Pulsera01");  // Nombre visible del dispositivo BLE
  BLEServer *pServer = BLEDevice::createServer();

  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_NOTIFY
                    );

  // Valor inicial de la característica
  pCharacteristic->setValue("activo");

  pService->start();

  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // Compatibilidad iOS
  pAdvertising->setMinPreferred(0x12);  // Compatibilidad iOS

  BLEDevice::startAdvertising();
  Serial.println("📡 Anunciando como Pulsera01...");
}

void loop() {
  // Aquí podrías cambiar el valor de la característica según sensores, botón, etc.
  delay(5000);
}
