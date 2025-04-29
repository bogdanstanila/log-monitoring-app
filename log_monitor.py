import csv
from datetime import datetime, timedelta
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

# Thresholds
WARNING_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)

def parse_log_file(file_path):
    """
    Parses the CSV log file and returns a list of log entries.
    Each entry is a dict with keys: timestamp, description, action, pid.
    """
    entries = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            timestamp_str, description, action, pid = row
            timestamp = datetime.strptime(timestamp_str.strip(), "%H:%M:%S")
            entries.append({
                'timestamp': timestamp,
                'description': description.strip(),
                'action': action.strip(),
                'pid': pid.strip()
            })
    print(f"Parsed {len(entries)} log entries.")
    # print (entries)
    # for entry in entries:
    #     print(f"Parsed entry: {entry}")
    return entries

def monitor_jobs(entries):
    """
    Processes log entries and monitors job durations.
    """
    job_start_times = {}
    job_reports = []

    for entry in entries:
        pid = entry['pid']
        timestamp = entry['timestamp']
        description = entry['description']

        if entry['action'] == 'START':
            job_start_times[pid] = (timestamp, description)
        elif entry['action'] == 'END':
            if pid not in job_start_times:
                logging.error(f"END without START for PID {pid}")
                continue
            start_time, start_description = job_start_times.pop(pid)
            duration = timestamp - start_time

            # Check thresholds
            if duration > ERROR_THRESHOLD:
                logging.error(f"Job '{start_description}' with PID {pid} took {duration}")
            elif duration > WARNING_THRESHOLD:
                logging.warning(f"Job '{start_description}' with PID {pid} took {duration}")
            else:
                logging.info(f"Job '{start_description}' with PID {pid} completed successfully in {duration}")

            job_reports.append({
                'pid': pid,
                'description': start_description,
                'duration': duration
            })
        else:
            logging.error(f"Unknown action {entry['action']} for PID {pid}")

    return job_reports

def main():
    log_file = 'logs.log'
    entries = parse_log_file(log_file)
    monitor_jobs(entries)

if __name__ == "__main__":
    main()
