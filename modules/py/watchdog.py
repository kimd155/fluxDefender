import time
import os
import fnmatch
import subprocess
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_PATHS = [
    r"C:\Windows\WinSxS\FileMaps",
    r"C:\Windows\System32",
    r"C:\Windows\SysWOW64",
    r"C:\Windows\System32\drivers"
]

FILES_TO_MONITOR = [
    "wow64_windows-defender*.manifest",
    "x86_windows-defender*.manifest",
    "amd64_windows-defender*.manifest",
    "SecurityAndMaintenance_Error.png",
    "SecurityAndMaintenance.png",
    "SecurityHealthSystray.exe",
    "SecurityHealthService.exe",
    "SecurityHealthHost.exe",
    "smartscreen.exe",
    "DWWIN.EXE",
    "wscadminui.exe",
    "GameBarPresenceWriter.exe",
    "DeviceCensus.exe",
    "CompatTelRunner.exe",
    "SgrmAgent.sys",
    "WdDevFlt.sys",
    "WdBoot.sys",
    "WdFilter.sys",
    "WdNisDrv.sys",
    "msseccore.sys",
    "MsSecFltWfp.sys",
    "MsSecFlt.sys",
    "wscsvc.dll",
    "wscproxystub.dll",
    "wscisvif.dll",
    "SecurityHealthProxyStub.dll",
    "smartscreen.dll",
    "smartscreenps.dll",
    "SecurityHealthCore.dll",
    "SecurityHealthSsoUdk.dll",
    "SecurityHealthUdk.dll",
    "SecurityHealthAgent.dll",
    "wscapi.dll",
    "smartscreen.dll",
    "smartscreen.exe",
    "smartscreenps.dll",
    "GameBarPresenceWriter.exe",
    "DeviceCensus.exe",
    "CompatTelRunner.exe"
]

current_directory = os.getcwd()
SDELETE_PATH = os.path.join(current_directory, 'binaries', 'sdelete64.exe')
logging.basicConfig(
    filename='file_watcher.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        for file_pattern in FILES_TO_MONITOR:
            if fnmatch.fnmatch(event.src_path, os.path.join(*WATCHED_PATHS, file_pattern)):
                logging.info(f"File detected: {event.src_path}")
                try:
                    command = [SDELETE_PATH, '-accepteula', '-r', '-f', event.src_path]
                    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    logging.info(f"Successfully deleted file {event.src_path}")
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error securely deleting file {event.src_path}: {e.stderr.decode()}")

class Watcher:
    def __init__(self):
        self.observer = Observer()
    
    def run(self):
        event_handler = Handler()
        for path in WATCHED_PATHS:
            self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()
        logging.info("File watcher started.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("File watcher stopped by user.")
            self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    w = Watcher()
    logging.info("Starting file watcher service.")
    w.run()
