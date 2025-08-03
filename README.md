# ProyectoCenfotec - AuraBLE System

Este proyecto implementa un sistema de comunicación y monitoreo usando **Bluetooth Low Energy (BLE)**, con dos dispositivos principales:

---

## 📦 Estructura

```
ProyectoCenfotec/
├── AuraBLE Band/         # Pulsera BLE (Beetle ESP32-C6)
│   └── Pulsera/
├── AuraBLE Hub/          # Hub BLE (IdeaBoard o AtomS3)
├── .gitignore
└── AuraBLE.code-workspace
```

---

## 🟢 AuraBLE Band (Pulsera)
- Envía eventos BLE: `pánico` y `vibración`
- Usa sensores físicos (botón, SW-520D)
- Bajo consumo con deep sleep

## 🟣 AuraBLE Hub
- Detecta proximidad BLE (RSSI)
- Recibe notificaciones de eventos
- Puede sincronizar el contenido del dispositivo conectado usando `sync_on_change.py`

---

## ⚙️ Requisitos

- Python 3.10+
- Instalar dependencias:
  ```bash
  pip install watchdog
  ```

---

## 🚀 Uso del script de sincronización

```bash
python sync_on_change.py
```

Monitorea el AtomS3 (unidad D:) y copia los cambios automáticamente a la carpeta del proyecto.

---
