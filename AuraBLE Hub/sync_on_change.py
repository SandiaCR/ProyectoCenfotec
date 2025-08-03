import time
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCE = "D:/"
DEST   = "C:/Users/mlean/OneDrive/Personal/Documentos/github/AuraBLE/AuraBLE Hub"
EXCLUDES = {"System Volume Information", ".Trashes", ".metadata_never_index", "boot_out.txt"}

def sync():
    print("🔄 Detectado cambio. Sincronizando...")
    if not os.path.exists(DEST):
        os.makedirs(DEST)

    for item in os.listdir(SOURCE):
        if item in EXCLUDES or item.startswith(".Trash"):
            continue

        src = os.path.join(SOURCE, item)
        dst = os.path.join(DEST, item)

        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    print("✅ Sincronización completada.\n")

class CambioHandler(FileSystemEventHandler):
    def on_modified(self, event):
        sync()

    def on_created(self, event):
        sync()

    def on_deleted(self, event):
        sync()

if __name__ == "__main__":
    if not os.path.exists(SOURCE):
        print("❌ El AtomS3 (D:) no está conectado.")
    else:
        print("👀 Observando cambios en AtomS3...")
        event_handler = CambioHandler()
        observer = Observer()
        observer.schedule(event_handler, path=SOURCE, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
