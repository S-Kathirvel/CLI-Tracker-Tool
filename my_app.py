import time
import threading
import pygetwindow as gw
import os

# Define the global variable to control the service
running = False
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt')
def write_log(active_window, window_time, total_time):
    # data = f"{active_window} time: {window_time} seconds\n Time spent on '{active_window.split(' - ')[0]}': {window_time:.2f} seconds\n Total time: {total_time} seconds\n\n"
    # print(data)
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(f'{active_window} time: {window_time} seconds\n')
        f.write(f"Time spent on '{active_window.split(' - ')[0]}': {window_time:.2f} seconds\n")
        f.write(f'Total time: {total_time} seconds\n\n')
        f.flush()

def track_time():
    active_window = None
    start_time = None
    total_time = 0
    url_time = 0

    try:
        while running:
            # Get the currently active window
            current_window = gw.getActiveWindow()

            if current_window is not None:
                current_title = current_window.title

                if active_window != current_title:
                    # A new window has been activated
                    if active_window and start_time:
                        # Calculate time spent in the previous window
                        elapsed_time = time.time() - start_time
                        total_time += elapsed_time
                        write_log(active_window, url_time, total_time)
                        if " - Brave" in active_window:
                            url_time += elapsed_time

                    # Update to the new window
                    active_window = current_title
                    start_time = time.time()

            time.sleep(1)  # Check every second

    except Exception as e:
        print(f"Error: {e}")
        stop_tracking()  # Ensure the service stops cleanly

    finally:
        if active_window and start_time:
            # Calculate final time for the last active window
            elapsed_time = time.time() - start_time
            total_time += elapsed_time
            write_log(active_window, elapsed_time, total_time)

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
if __name__ == "__main__":
    start_tracking()

    while running:
        time.sleep(1)  # Keep the script running while the service is active

    # When `running` is set to False, the loop will break and the script will exit
