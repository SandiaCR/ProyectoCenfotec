#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define SERVICE_UUID        "12345678-1234-5678-1234-56789abcdef0"
#define CHARACTERISTIC_UUID "12345678-1234-5678-1234-56789abcdef1"

BLECharacteristic* pCharacteristic;

void setup() {
  Serial.begin(115200);
  Serial.println("🔧 Iniciando BLE...");

  BLEDevice::init("Pulsera01");  // Nombre que aparece en escaneo
  BLEServer* pServer = BLEDevice::createServer();

  BLEService* pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ |
    BLECharacteristic::PROPERTY_NOTIFY
  );

  pCharacteristic->setValue("PRUEBA123");
  pService->start();

  BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // Compatibilidad iOS
  pAdvertising->setMinPreferred(0x12);

  BLEDevice::startAdvertising();
  Serial.println("📡 Pulsera01 anunciando PRUEBA123...");
}

void loop() {
  static bool toggle = false;

  if (toggle) {
    pCharacteristic->setValue("valorA");
  } else {
    pCharacteristic->setValue("valorB");
  }
  toggle = !toggle;

  pCharacteristic->notify();  // Envía valor si alguien está suscrito
  Serial.println("📤 Notificación enviada.");

  delay(5000);
}
