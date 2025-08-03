import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import Advertisement

ble = BLERadio()

print("🔍 Escaneando BLE...")

device = None
for adv in ble.start_scan(Advertisement, timeout=10):
    if adv.complete_name and "Pulsera01" in adv.complete_name:
        device = adv
        print(f"📡 Detectado: {adv.complete_name}")
        break

ble.stop_scan()

if not device:
    print("❌ Pulsera01 no encontrada.")
else:
    print("🔗 Conectando...")
    try:
        connection = ble.connect(device)
        print("✅ Conectado.")

        # 🧩 Servicios y características disponibles
        for service in connection.remote_services:
            print(f"🧩 Servicio UUID: {service.uuid}")
            for char in service.characteristics:
                try:
                    val = char.read_value()
                    decoded = val.decode("utf-8") if isinstance(val, bytes) else str(val)
                    print(f"  ↳ Característica: {char.uuid} → {decoded}")
                except Exception as e:
                    print(f"  ↳ Característica: {char.uuid} → no legible: {e}")

        connection.disconnect()
        print("🔌 Desconectado.")

    except Exception as e:
        print(f"⚠️ Error: {e}")
