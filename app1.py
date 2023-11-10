import psutil
from datetime import datetime
import os
import time

def log_activity(log_file, process_info, start_time, end_time, date):
    with open(log_file, 'a') as f:
        f.write(f"Date: {date}, Process: {process_info}, Start Time: {start_time}, End Time: {end_time}\n")

def list_all_processes_and_track(log_file, interval=60):
    script_directory = os.path.dirname(os.path.abspath(__file__))

    while True:
        current_time = datetime.now()
        all_processes = [p.info for p in psutil.process_iter(['pid', 'name'])]
        current_time_str = current_time.strftime('%H:%M:%S')
        current_date_str = current_time.strftime('%Y-%m-%d')

        with open(log_file, 'a') as f:
            f.write(f"\nTime: {current_time_str}\n")

        for process_info in all_processes:
            log_activity(log_file, process_info, current_time_str, None, current_date_str)

        # Wait for the specified interval before checking again
        time.sleep(interval)

# Example usage
if __name__ == "__main__":
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'activity_log.txt')
    
    print("Listing all processes and tracking...")
    list_all_processes_and_track(log_file)
