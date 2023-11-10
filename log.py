import psutil
import time
from datetime import datetime, timedelta
import os

def log_activity(log_file, app_name, start_time, end_time, date):
    with open(log_file, 'a') as f:
        log_entry = f"Date: {date}, Application: {app_name}, Start Time: {start_time}, End Time: {end_time}\n"
        f.write(log_entry)
        print(log_entry)

def track_activity(log_file, app_to_track="chrome", start_hour=9, end_hour=12, interval=60):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    while True:
        current_time = datetime.now()
        
        # Check if the current time is within the specified range
        if start_hour <= current_time.hour < end_hour:
            # Get the current active processes
            all_processes = [p.name() for p in psutil.process_iter(['pid', 'name'])]

            # Debug print to check all processes
            print(f"All processes: {all_processes}")

            # Wait for the specified interval
            time.sleep(interval)

            # Check for changes in active processes
            new_processes = {p.name(): p for p in psutil.process_iter(['pid', 'name'])}

            # Find started processes
            started_processes = [app for app in new_processes.keys() if app_to_track.lower() in app.lower() and app not in all_processes]

            # Find stopped processes
            stopped_processes = [app for app in all_processes if app_to_track.lower() in app.lower() and app not in new_processes]

            # Log the activity
            current_time_str = current_time.strftime('%H:%M:%S')
            current_date_str = current_time.strftime('%Y-%m-%d')

            print(f"Current Time: {current_time_str}, Started Processes: {started_processes}, Stopped Processes: {stopped_processes}")

            for app_name in started_processes:
                log_activity(log_file, app_name, current_time_str, None, current_date_str)
            for app_name in stopped_processes:
                log_activity(log_file, app_name, None, current_time_str, current_date_str)
        else:
            # Sleep until the next day to resume tracking
            next_day = current_time.replace(hour=start_hour, minute=0, second=0, microsecond=0) + timedelta(days=1)
            time.sleep((next_day - current_time).seconds)

# Example usage
if __name__ == "__main__":
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    script_directory = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(desktop_path, 'activity_log.txt')
    print(f"Log file: {log_file}")
    print("Starting tracking...")
    track_activity(log_file)
