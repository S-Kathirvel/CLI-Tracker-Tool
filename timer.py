import argparse
import time
import os
from time_functions import (
    format_time_delta,
    display_timer_status_for_10_seconds,
    timer_is_running,
    write_start_time_to_log,
    write_stop_time_to_log
)

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

# Handle commands
if args.command == "start_timer":
    if timer_is_running(pid_file):
        print("Timer is already running.")
        with open(pid_file, "r") as f:
            start_time = float(f.read().strip())
        display_timer_status_for_10_seconds(start_time)
    else:
        start_time = time.time()
        write_start_time_to_log(start_time, log_file)
        with open(pid_file, "w") as f:
            f.write(str(start_time))
        print("Timer started.")

elif args.command == "stop_timer":
    if not timer_is_running(pid_file):
        print("No timer is running.")
    else:
        stop_time = time.time()
        with open(pid_file, "r") as f:
            start_time = float(f.read().strip())
        write_stop_time_to_log(start_time, stop_time, log_file)
        os.remove(pid_file)  # Remove the PID file
        print(f"Timer stopped. Elapsed time: {format_time_delta(stop_time - start_time)}.")

elif args.command == "elapsed_time":
    if timer_is_running(pid_file):
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
