import unittest
from datetime import datetime, timedelta
from log_monitor import monitor_jobs

class TestLogMonitor(unittest.TestCase):
    def test_monitor_jobs(self):
        # 3 test jobs:
        entries = [
            # Job 1: 1 min (should be OK)
            {'timestamp': datetime.strptime('10:00:00', "%H:%M:%S"), 'description': 'task short', 'action': 'START', 'pid': '001'},
            {'timestamp': datetime.strptime('10:01:00', "%H:%M:%S"), 'description': 'task short', 'action': 'END', 'pid': '001'},

            # Job 2: 6 min (should trigger WARNING)
            {'timestamp': datetime.strptime('11:00:00', "%H:%M:%S"), 'description': 'task warning', 'action': 'START', 'pid': '002'},
            {'timestamp': datetime.strptime('11:06:00', "%H:%M:%S"), 'description': 'task warning', 'action': 'END', 'pid': '002'},

            # Job 3: 11 min (should trigger ERROR)
            {'timestamp': datetime.strptime('12:00:00', "%H:%M:%S"), 'description': 'task error', 'action': 'START', 'pid': '003'},
            {'timestamp': datetime.strptime('12:11:00', "%H:%M:%S"), 'description': 'task error', 'action': 'END', 'pid': '003'},
        ]

        reports = monitor_jobs(entries)

        # Assert that we got exactly 3 reports
        self.assertEqual(len(reports), 3)

        # Check each duration individually
        self.assertEqual(reports[0]['pid'], '001')
        self.assertLess(reports[0]['duration'], timedelta(minutes=5))  # 1 min is OK

        self.assertEqual(reports[1]['pid'], '002')
        self.assertGreater(reports[1]['duration'], timedelta(minutes=5))  # 6 min should WARN
        self.assertLess(reports[1]['duration'], timedelta(minutes=10))    # Still less than ERROR

        self.assertEqual(reports[2]['pid'], '003')
        self.assertGreater(reports[2]['duration'], timedelta(minutes=10))  # 11 min should ERROR

if __name__ == '__main__':
    unittest.main()
