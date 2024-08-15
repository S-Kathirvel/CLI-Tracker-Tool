import pygetwindow as gw
import time
import os
import threading
# from session_functions import format_time_delta

def monitor_windows(session_name):
    """
    Monitors the currently active window and logs its details to a session-specific temporary file.
    
    Args:
        session_name (str): The name of the session to track windows for.
    """
    WINDOW_TEMP_FILE = f"{session_name}_window.tmp"
    
    with open(WINDOW_TEMP_FILE, "w") as file:
        file.write(f"Session: {session_name}\n")
        # file.write("Start time: " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n")
        file.write("Windows:\n")
    
    print(f"Tracking windows for session '{session_name}'.")

    def track_windows():
        """
        Continuously monitor the active window and update the log.
        """
        previous_window = None
        while True:
            active_window_details = get_active_window_details()
            if active_window_details != previous_window:
                update_cumulative_time(session_name, active_window_details)
                previous_window = active_window_details
            time.sleep(1)  # Adjust the sleep duration as needed

    # Start tracking in a separate thread
    monitor_thread = threading.Thread(target=track_windows)
    monitor_thread.daemon = True
    monitor_thread.start()

def update_cumulative_time(session_name, window_name):
    """
    Updates the cumulative time spent on a given window or tab in the session-specific temporary file.
    
    Args:
        session_name (str): The name of the session to track windows for.
        window_name (str): The name of the window or tab to update.
    """
    WINDOW_TEMP_FILE = f"{session_name}_window.tmp"
    current_time = time.time()
    
    if not os.path.exists(WINDOW_TEMP_FILE):
        print(f"Temporary window tracking file '{WINDOW_TEMP_FILE}' does not exist.")
        return
    
    # Append the current window time to the temporary file
    with open(WINDOW_TEMP_FILE, "a") as file:
        file.write(f"Window: {window_name}, Time: {current_time}\n")

def get_active_window_details():
    """
    Retrieves details of the currently active window.
    
    Returns:
        str: A formatted string containing the application name, folder (if any), and file name (if applicable).
    """
    active_window = gw.getActiveWindow()
    
    if not active_window:
        return "No active window found."

    window_title = active_window.title
    application_name = window_title.split(' - ')[0] if ' - ' in window_title else window_title
    
    # Placeholder: Implement logic to determine folder and file name if applicable
    folder = "No folder info"  # Implement folder extraction if needed
    file_name = "No file info"  # Implement file extraction if needed

    return f"{application_name} - {folder} - {file_name}"


