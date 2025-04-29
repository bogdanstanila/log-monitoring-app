# Log Monitor Application

## Description

This application reads a log file `logs.log`, tracks the start and end of jobs using their PIDs, calculates how long each job took, and logs warnings or errors if they exceed specified thresholds.

- **Warning**: Job duration > 5 minutes
- **Error**: Job duration > 10 minutes

## How to Run

1. Place your `logs.log` file in the same directory as the `log_monitor.py` script.

2. Run the following command to execute the log monitor:
   ```bash
   python3 log_monitor.py

## Run the Tests
- Unit tests are available for validating the behavior of the log monitoring application.

- Run the tests using the following command:
    ```bash
    python3 -m unittest test_log_monitor.py

## Edge Cases and Assumptions

The application handles the following edge cases that may occur in the log file:

### 1. **END without a matching START**

These are considered **invalid** jobs because we don’t know when they began.

- The entry is **skipped** in duration calculation.
- A **warning** is logged to notify that an END entry has no corresponding START.

**Example log entry:**
12:10:45, scheduled task ghost, END,99887

**Logged warning:**
WARNING: END found for PID 99887 without a matching START.

### 2. **START without a matching END**

These are **incomplete jobs**, possibly due to system failure, log corruption, or a process still running.

- The entry is **skipped** in duration calculation.
- A **warning** is logged to highlight the missing END.

**Example log entry:**
13:03:12, background sync, START,55321

**Logged warning:**
WARNING: START found for PID 55321 but no END entry was found.

### 3. **Jobs that span across midnight**

Some jobs start before midnight and finish after. Since the log file does not include dates, this must be inferred.

- The program correctly calculates the duration by **adding 24 hours** to the END time if it is **earlier than the START time**.
- These jobs are treated as valid and monitored like all others.

**Example log entries:**
23:58:00, long nightly backup, START,44000
00:04:00, long nightly backup, END,44000

**Computed duration:**
6 minutes

**Logged warning (if applicable):**
WARNING: Job 'long nightly backup' with PID 44000 took 6 minutes.


### Summary Table

| Scenario                  | Behavior                 | Logged?     | Included in Report? |
|---------------------------|--------------------------|-------------|----------------------|
| END without START         | Ignored                  | Warning     | ❌ No                |
| START without END         | Ignored                  | Warning     | ❌ No                |
| Spans midnight            | Time adjusted correctly  | Warning/Error if thresholds hit | ✅ Yes        |