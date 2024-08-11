# time_functions.py

import time
import os
from datetime import datetime, timedelta

# Format the time delta into days, hours, minutes, and seconds
def format_time_delta(seconds):
    """Convert seconds to days, hours, minutes, and seconds."""
    delta = timedelta(seconds=seconds)
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d:{hours}h:{minutes}m:{seconds}s"

# Display the current timer status for 10 seconds
def display_timer_status_for_10_seconds(start_time):
    """Display the current timer status for 10 seconds."""
    print("Timer status:")
    for _ in range(10):
        current_time = time.time()
        elapsed_time = current_time - start_time
        formatted_time = format_time_delta(elapsed_time)
        print(f"\rElapsed: {formatted_time}", end="")
        time.sleep(1)
    print()  # To move to the next line after the loop ends

# Check if the timer is currently running
def timer_is_running(pid_file):
    """Check if the timer is currently running."""
    return os.path.exists(pid_file)

# Write the start time to the log file
def write_start_time_to_log(start_time, log_file):
    """Write the start time to the log file."""
    device_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, "a") as f:
        f.write(f"Start: {device_time})\n")  # (Epoch: {start_time})\n")

# Write the stop time and elapsed time to the log file
def write_stop_time_to_log(start_time, stop_time, log_file):
    """Write the stop time and elapsed time to the log file."""
    device_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elapsed_time = stop_time - start_time
    formatted_elapsed = format_time_delta(elapsed_time)
    
    with open(log_file, "a") as f:
        f.write(f"Stop: {device_time} (Epoch: {stop_time})\n")
        f.write(f"Elapsed: {formatted_elapsed}\n")
