import argparse
import time
import os
from datetime import datetime, timedelta

# Set up argument parser
parser = argparse.ArgumentParser(description="Simple CLI Time Tracking Tool")
subparsers = parser.add_subparsers(dest="command", help="Available commands")

# Define start command
subparsers.add_parser("start_timer", help="Start the Timer")

# Define stop command
subparsers.add_parser("stop_timer", help="Stop the Timer")

# Define elapsed command
subparsers.add_parser("elapsed_time", help="Show elapsed time since the timer started")

# Define log command
subparsers.add_parser("show_log", help="Show the log of all time intervals")

subparsers.add_parser("list", help="Listing all available commands")
# Parse the arguments
args = parser.parse_args()

# File to store the start time and logs
log_file = "time_log.txt"
pid_file = "timer_pid.txt"

def format_time_delta(seconds):
    """Convert seconds to days, hours, minutes, and seconds."""
    delta = timedelta(seconds=seconds)
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d:{hours}h:{minutes}m:{seconds}s"

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

def timer_is_running():
    """Check if the timer is currently running."""
    return os.path.exists(pid_file)

def write_start_time_to_log(start_time):
    """Write the start time to the log file."""
    device_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, "a") as f:
        f.write(f"Start: {device_time})\n")# (Epoch: {start_time})\n")

def write_stop_time_to_log(start_time, stop_time):
    """Write the stop time and elapsed time to the log file."""
    device_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elapsed_time = stop_time - start_time
    formatted_elapsed = format_time_delta(elapsed_time)
    
    with open(log_file, "a") as f:
        f.write(f"Stop: {device_time} (Epoch: {stop_time})\n")
        f.write(f"Elapsed: {formatted_elapsed}\n")

# Handle commands
if args.command == "start_timer":
    if timer_is_running():
        print("Timer is already running.")
        with open(pid_file, "r") as f:
            start_time = float(f.read().strip())
        display_timer_status_for_10_seconds(start_time)
    else:
        start_time = time.time()
        write_start_time_to_log(start_time)
        with open(pid_file, "w") as f:
            f.write(str(start_time))
        print("Timer started.")

elif args.command == "stop_timer":
    if not timer_is_running():
        print("No timer is running.")
    else:
        stop_time = time.time()
        with open(pid_file, "r") as f:
            start_time = float(f.read().strip())
        write_stop_time_to_log(start_time, stop_time)
        os.remove(pid_file)  # Remove the PID file
        print(f"Timer stopped. Elapsed time: {format_time_delta(stop_time - start_time)}.")

elif args.command == "elapsed_time":
    if timer_is_running():
        with open(pid_file, "r") as f:
            start_time = float(f.read().strip())
        display_timer_status_for_10_seconds(start_time)
    else:
        print("No timer is running.")

elif args.command == "show_log":
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            print(f.read())
    else:
        print("No log file found.")

elif args.command == "list":
    parser.print_help()
    exit(1)
