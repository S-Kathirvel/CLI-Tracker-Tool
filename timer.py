import pygetwindow as gw
import time
import threading

def write_log(active_window,window_time,total_time):
    with open('log.txt', 'a') as f:
        f.write(f'{active_window} time: {window_time} seconds\n')
        f.write(f"Time spent on '{active_window.split(' - ')[0]}': {window_time:.2f} seconds")
        f.write(f'Total time: {total_time} seconds\n')

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
                        write_log(active_window,url_time,total_time)
                        if " - Brave" in active_window:
                            url_time += elapsed_time
                            # print(f"Time spent on '{active_window.split(' - ')[0]}': {elapsed_time:.2f} seconds")


                    # Update to the new window
                    active_window = current_title
                    start_time = time.time()

            time.sleep(1)  # Check every second

    except KeyboardInterrupt:
        print("Timer stopped")
        if active_window and start_time:
            # Calculate final time for the last active window
            elapsed_time = time.time() - start_time
            total_time += elapsed_time
            print(f"Final time spent on '{active_window}': {elapsed_time:.2f} seconds")
            if " - Google Chrome" in active_window:
                url_time += elapsed_time
                print(f"Final time spent on '{active_window.split(' - ')[0]}': {elapsed_time:.2f} seconds")

        write_log(active_window,elapsed_time,total_time)
        # print(f"Total time spent in active window: {total_time:.2f} seconds")
        # print(f"Total time spent in browser windows: {url_time:.2f} seconds")


def start_tracking():
    global running
    running = True
    tracker_thread = threading.Thread(target=track_time)
    tracker_thread.daemon = True
    tracker_thread.start()


def stop_tracking():
    global running
    running = False


if __name__ == "__main__":
    print("Press Enter to start the timer and Ctrl+C to stop it.")
    input()
    start_tracking()
    
    try:
        while True:
            time.sleep(1)  # Keep the script running

    except KeyboardInterrupt:
        stop_tracking()
