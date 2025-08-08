import time
import json
import os
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import Advertisement

# ===== Leer variables de entorno =====
WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASS = os.getenv("WIFI_PASS")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# ===== BLE =====
ble = BLERadio()

DISPOSITIVOS_MONITOREADOS = {
    "Pulsera01": {
        "contador_estable": 0,
        "umbral_rssi": -50,
        "cerca": False,
    }
}
LECTURAS_ESTABLES = 3

# ===== Conexión WiFi ====  =s
print("📡 Conectando a WiFi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASS)
print("✅ Conectado a", WIFI_SSID)

# ===== MQTT =====
pool = socketpool.SocketPool(wifi.radio)
mqtt_client = MQTT.MQTT(
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    socket_pool=pool,
    ssl_context=None
)
mqtt_client.connect()
print("✅ MQTT conectado a", MQTT_BROKER)
print("🔍 Escaneando continuamente...")

while True:
    for adv in ble.start_scan(Advertisement, timeout=1):
        nombre = adv.complete_name or ""
        rssi = adv.rssi

        if nombre in DISPOSITIVOS_MONITOREADOS:
            dispositivo = DISPOSITIVOS_MONITOREADOS[nombre]
            cerca_nuevo = rssi > dispositivo["umbral_rssi"]

            if cerca_nuevo != dispositivo["cerca"]:
                dispositivo["contador_estable"] += 1
                if dispositivo["contador_estable"] >= LECTURAS_ESTABLES:
                    dispositivo["cerca"] = cerca_nuevo
                    dispositivo["contador_estable"] = 0
                    estado = "CERCA" if cerca_nuevo else "LEJOS"
                    t = time.localtime()
                    hora = "{:02}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec)
                    payload = {
                        "dispositivo": "Pulsera01",  # antes era 'nombre'
                        "evento": estado,           # antes era 'estado'
                        "timestamp": hora
                    }
                    mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
                    print(f"📤 Enviado MQTT: {payload}")
            else:
                dispositivo["contador_estable"] = 0

    ble.stop_scan()
    time.sleep(0.2)
