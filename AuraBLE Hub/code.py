import time
from adafruit_ble import BLERadio
from adafruit_ble.uuid import UUID

ble = BLERadio()
print("🔍 Buscando Pulsera01 (por MAC)...")

SERVICE_UUID = UUID("0000180F-0000-1000-8000-00805F9B34FB")   # Battery Service
CHAR_UUID    = UUID("00002A19-0000-1000-8000-00805F9B34FB")   # Battery Level

PULSERA_MAC = "da9307bdf5f0"  # <- tu MAC, minúsculas, sin ':'

while True:
    print("Escaneando BLE...")
    for adv in ble.start_scan(timeout=10):
        mac = adv.address.address_bytes.hex().lower()
        if mac == PULSERA_MAC:
            print(f"✅ Pulsera01 encontrada (MAC={mac}, RSSI={adv.rssi})")
            try:
                print("Intentando conectar...")
                connection = ble.connect(adv, timeout=10)
                print("¡Conectado!")
                print("Descubriendo servicios BLE...")
                connection.discover_services()

                print("=== Servicios encontrados ===")
                for service in connection.services:
                    print(f"Service: {service} | UUID: {service.uuid} | type: {type(service.uuid)}")
                    for char in service.characteristics:
                        print(f"  Characteristic: {char} | UUID: {char.uuid} | props: {char.properties}")

                # Buscar Battery Service
                found_service = None
                for service in connection.services:
                    if str(service.uuid).lower() == str(SERVICE_UUID).lower():
                        found_service = service
                        break
                if not found_service:
                    print("❌ Servicio de batería no encontrado.")
                else:
                    print("Servicio de batería encontrado.")
                    found_char = None
                    for char in found_service.characteristics:
                        if str(char.uuid).lower() == str(CHAR_UUID).lower():
                            found_char = char
                            break
                    if found_char:
                        try:
                            battery_val = found_char.value[0]
                            print(f"🔋 Nivel de batería: {battery_val}%")
                        except Exception as e:
                            print("⚠️ Error leyendo valor de batería:", e)
                    else:
                        print("❌ Characteristic de batería no encontrada.")
                connection.disconnect()
                print("Desconectado.\n")
            except Exception as e:
                print("⚠️ Error al conectar/leer:", e)
            time.sleep(5)
            break
    ble.stop_scan()
    time.sleep(2)

