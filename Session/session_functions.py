import time
import os
from datetime import datetime, timedelta
from window_tracking import monitor_windows

MAIN_LOG_FILE = "session_log.txt"

def format_time_delta(seconds):
    """Convert seconds to days, hours, minutes, and seconds."""
    delta = timedelta(seconds=seconds)
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d:{hours:02}h:{minutes:02}m:{seconds:02}s"

def start_session(session_name):
    SESSION_TEMP_FILE = f"{session_name}.tmp"


    with open(SESSION_TEMP_FILE, "w") as log:
        start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"Session: {session_name}\n")
        log.write(f"Start time: {start_time}\n")

    print(f"Session '{session_name}' started at {start_time}.")
    monitor_windows(session_name)    

def end_session(session_name):
    """
    Ends a session, calculates the elapsed time, and writes data to the main log file.
    
    Args:
        session_name (str): The name of the session to end.
    """
    WINDOW_TEMP_FILE = f"{session_name}_window.tmp"
    SESSION_TEMP_FILE = f"{session_name}.tmp"

    if not os.path.exists(SESSION_TEMP_FILE):
        print(f"No active session named '{session_name}' found.")
        return

    # Read session log file
    with open(SESSION_TEMP_FILE, "r") as log:
        lines = log.readlines()
    
    # Extract start time and calculate elapsed time
    start_time_str = lines[1].strip().split(": ", 1)[1]
    start_time = time.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    start_time_epoch = time.mktime(start_time)
    
    end_time = time.strftime('%Y-%m-%d %H:%M:%S')
    end_time_struct = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    end_time_epoch = time.mktime(end_time_struct)
    
    elapsed_time = end_time_epoch - start_time_epoch
    elapsed = format_time_delta(elapsed_time)

    # Update session log file with end time and elapsed time
    with open(SESSION_TEMP_FILE, "a") as log:
        log.write(f"End time: {end_time}\n")
        log.write(f"Elapsed time: {elapsed} seconds\n")

    # Handle window tracking
    if os.path.exists(WINDOW_TEMP_FILE):
        with open(WINDOW_TEMP_FILE, "r") as win_log:
            window_lines = win_log.readlines()
    else:
        window_lines = []    

    # Write session and elapsed time data to the main log file
    with open(MAIN_LOG_FILE, "a") as main_log:
        main_log.writelines(lines)
        main_log.write(f"End time: {end_time}\n")
        main_log.write(f"Elapsed time: {elapsed} seconds\n\n")
        main_log.write("Window Tracking:\n")
        main_log.writelines(window_lines)
        main_log.write("\n")
    
    # Remove the temporary file
    os.remove(SESSION_TEMP_FILE)
    if os.path.exists(WINDOW_TEMP_FILE):
        os.remove(WINDOW_TEMP_FILE)
    
    print(f"Session '{session_name}' ended at {end_time}. Elapsed time: {elapsed}.")

def display_timer_status_for_10_seconds(session_name):
    SESSION_TEMP_FILE = f"{session_name}.tmp"
    
    if not os.path.exists(SESSION_TEMP_FILE):
        print(f"No active session named '{session_name}' found.")
        return

    # Read the start time from the temporary log file
    with open(SESSION_TEMP_FILE, "r") as log:
        lines = log.readlines()
        start_time_str = lines[1].strip().split(": ", 1)[1]
        start_time = time.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        start_time = time.mktime(start_time)  # Convert to timestamp

    # Display the current elapsed time for 10 seconds
    print(f"Timer status for session '{session_name}':")
    for _ in range(10):
        current_time = time.time()
        elapsed_time = current_time - start_time
        formatted_time = format_time_delta(elapsed_time)
        print(f"\rElapsed: {formatted_time}", end="")
        time.sleep(1)
    print()