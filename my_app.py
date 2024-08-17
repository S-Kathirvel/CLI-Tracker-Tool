import json
import time
import threading
import pygetwindow as gw
import os

# Define the global variable to control the service
running = False
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt')
ACTIVE_WINDOW_THRESHOLD = 5  # Threshold time in seconds
base_format = json.loads(open('item_format.json').read())


def write_log(active_window, window_time, total_time):
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(f'{active_window} time: {window_time} seconds\n')
        f.write(f"Time spent on '{active_window.split(' - ')[0]}': {window_time:.2f} seconds\n")
        f.write(f'Total time: {total_time} seconds\n\n')
        f.flush()

def initialize_record(session_name,PID,mode,start_time):
    with open('storage-format.json','r+') as fh:
        data = json.load(fh)
        base_format['mode'] = mode
        base_format['PID'] = PID
        base_format['start-time'] = start_time
        data[session_name] = base_format
        json.dump(data,fh,indent=4,ensure_ascii=True)
        fh.flush()

def update_stats(session_name,total_time,app_time,idle_time,epoch=None):
    with open('storage-format.json','r') as fh:
        data = json.load(fh)
        data[session_name]['Total-time'] = total_time
        data[session_name]['application_time'] = app_time
        data[session_name]['idle_time'] = idle_time
        data[session_name]['epoch'] = epoch
        fh.flush()
    with open('storage-format.json','w') as fh:
        json.dump(data,fh,indent=4,ensure_ascii=True)
        fh.flush()



def track_time():
    active_window = None
    start_time = None
    total_time = 0
    url_time = 0
    apps = {}
    try:
        while running:
            # Get the currently active window
            current_window = gw.getActiveWindow()

            if current_window is not None:
                current_title = current_window.title
                if current_title not in apps:
                    apps[current_title] = 0  # Initialize the app in the dictionary

                if active_window != current_title:
                    # A new window has been activated
                    if active_window and start_time:
                        # Calculate time spent in the previous window
                        elapsed_time = time.time() - start_time
                        if elapsed_time > ACTIVE_WINDOW_THRESHOLD:
                            total_time += elapsed_time
                            apps[active_window] += elapsed_time  # Increment time in the apps dictionary
                            write_log(active_window, elapsed_time, total_time)
                            if " - Brave" in active_window:
                                url_time += elapsed_time

                    # Update to the new window
                    active_window = current_title
                    start_time = time.time()
            update_stats("session-1",total_time,apps,0,95301)
            time.sleep(1)  # Check every second

    except Exception as e:
        print(f"Error: {e}")
        stop_tracking()  # Ensure the service stops cleanly

    finally:
        if active_window and start_time:
            # Calculate final time for the last active window
            elapsed_time = time.time() - start_time
            if elapsed_time > ACTIVE_WINDOW_THRESHOLD:
                total_time += elapsed_time
                apps[active_window] += elapsed_time  # Increment time in the apps dictionary
                write_log(active_window, elapsed_time, total_time)

        # Optional: Log total time spent per app at the end
        with open(LOG_FILE_PATH, 'a') as f:
            f.write('Total time spent per application:\n')
            for app, time_spent in apps.items():
                f.write(f'{app}: {time_spent:.2f} seconds\n')

def start_tracking():
    global running
    running = True
    tracker_thread = threading.Thread(target=track_time)
    tracker_thread.daemon = True  # Allow the thread to exit when the main program exits
    tracker_thread.start()

def stop_tracking():
    global running
    running = False

# Ensure the service runs continuously in the background
def run_tracker():7
    start_tracking()

    while running:
        time.sleep(1)  # Keep the script running while the service is active

    # When `running` is set to False, the loop will break and the script will exit
