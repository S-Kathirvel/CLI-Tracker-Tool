import sys
import time
import os
# import multiprocessing
from pid import PidFile, PidFileError
import subprocess

PID_FILE = "my_app.pid"

def main():
    while True:
        with open("service_log.txt", "a") as f:
            f.write("Service is running...\n")
        time.sleep(10)

def start_service():
    try:
        with PidFile(pidname=PID_FILE):
            process = subprocess.Popen(['python', 'my_app.py'], creationflags=subprocess.CREATE_NO_WINDOW)
            # process.start()
            with open(PID_FILE, "w") as f:
                f.write(str(process.pid))
            print(f"Service started with PID {process.pid}. Running in the background.")
    except PidFileError:
        print("Service is already running.")

def stop_service():
    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        if os.name == 'nt':  # Windows
            os.system(f"taskkill /PID {pid} /F")
        else:  # Unix-based systems
            os.kill(pid, 15)
        os.remove(PID_FILE)
        print("Service stopped")
    except FileNotFoundError:
        print("Service is not running.")
    except ProcessLookupError:
        print("No such process. Removing stale PID file.")
        os.remove(PID_FILE)

def status_service():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
        print(f"Service is running with PID {pid}")
    else:
        print("Service is not running")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: app_name start|stop|status")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "start":
        start_service()
    elif command == "stop":
        stop_service()
    elif command == "status":
        status_service()
    else:
        print("Unknown command")
