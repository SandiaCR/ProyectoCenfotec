#include <WiFi.h>
#include <PubSubClient.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>

// --- WiFi & MQTT ---
const char* ssid = "Ap31";
const char* password = "Mau*30420";
const char* mqtt_server = "192.168.1.100"; // IP del Pi
WiFiClient espClient;
PubSubClient client(espClient);

// --- BLE ---
BLEScan* pBLEScan;
#define SCAN_TIME 1 // segundos

// Dispositivo a vigilar
String targetName = "Pulsera01";
int umbralRSSI = -50;

void setup_wifi() {
  delay(10);
  Serial.println("📡 Conectando WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("🔄 Conectando MQTT...");
    if (client.connect("NodoESP32")) {
      Serial.println("✅ Conectado");
    } else {
      Serial.print("❌ Error: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);

  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setActiveScan(true);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  BLEScanResults foundDevices = pBLEScan->start(SCAN_TIME, false);
  for (int i = 0; i < foundDevices.getCount(); i++) {
    BLEAdvertisedDevice device = foundDevices.getDevice(i);
    if (device.haveName() && device.getName() == targetName) {
      int rssi = device.getRSSI();
      String estado = (rssi > umbralRSSI) ? "CERCA" : "LEJOS";
      String payload = "{\"nombre\":\"" + targetName + "\",\"rssi\":" + String(rssi) + ",\"estado\":\"" + estado + "\"}";
      client.publish("hogar/sensores", payload.c_str());
      Serial.println("📤 MQTT: " + payload);
    }
  }
}
