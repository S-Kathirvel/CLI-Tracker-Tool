import os
import time
import argparse
from session_functions import (
    display_timer_status_for_10_seconds,
    start_session,
    end_session
)

from window_tracking import get_active_window_details



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Session Manager Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    start_cmd = subparsers.add_parser("start_session", help="Start the session")
    start_cmd.add_argument("session_name", type=str, help="Name of the session to start")

    end_cmd = subparsers.add_parser("end_session", help="End the session")
    end_cmd.add_argument("session_name", type=str, help="Name of the session to end")

    status_cmd = subparsers.add_parser("status", help="To see how long the session is running")
    status_cmd.add_argument("session_name", type=str, help="Name of the session to see status")


    args = parser.parse_args()

    if args.command == "start_session":
        start_session(args.session_name)
    elif args.command == "end_session":
        end_session(args.session_name)
    elif args.command == "status":
        display_timer_status_for_10_seconds(args.session_name)
        # print(get_active_window_details())
    else:
        parser.print_help()
