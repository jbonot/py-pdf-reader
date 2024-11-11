import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ok_berichten_auto.auto_download_pdf import activate_app, download_file, go_to_calendar, go_to_patient, go_to_report

script_dir = os.path.dirname(__file__)
# Sample class for handling test cases and functions
class TestAutoDownloadPdf:
    config_path = os.path.join(script_dir, '..', '..', 'config.ini')
    dates_path = os.path.join(script_dir, 'auto_download_pdf.dates.txt')

    def __init__(self):
        # You could load your date entries here
        self.entries = self.load_dates(self.dates_path)

    def load_dates(self, filename):
        """Load dates from a file (mocked here)"""
        entries = []
        with open(filename, 'r') as file:
            for line in file.readlines():
                fields = line.strip().split('\t')
                if len(fields) > 1:
                    date_parts = fields[0].split('/')
                    entries.append({
                        'fullDate': fields[0],
                        'day': date_parts[0],
                        'month': date_parts[1],
                        'year': date_parts[2],
                        'name': fields[1]
                    })
        return entries

    def assert_test(self, result, test):
        """Custom assert function for test results"""
        if result:
            print(f"Pass\t{test}")
        else:
            print(f"Fail\t{test}")

    def test_activate_app(self):
        """Test ActivateApp function"""
        result = activate_app(self.config_path)
        self.assert_test(result, 'TestActivateApp')

    def test_download_file(self):
        """Test DownloadFile function"""
        result = download_file()
        self.assert_test(result, 'TestDownloadFile')

    def test_go_to_report(self):
        """Test GoToReport function"""
        result = go_to_report(self.entries[0]['fullDate'])  # Use the first entry for testing
        self.assert_test(result, 'TestGoToReport')

    def test_go_to_calendar(self):
        """Test GoToCalendar function"""
        result = go_to_calendar(self.entries[0])  # Use the first entry for testing
        self.assert_test(result, 'TestGoToCalendar')

    def test_go_to_patient(self):
        """Test GoToPatient function"""
        result = go_to_patient(0, 0)  # Example of calling this function
        self.assert_test(result, 'TestGoToPatient')

    def run_tests(self):
        """Run all tests"""
        self.test_activate_app()
        # self.test_go_to_calendar()
        # self.test_go_to_report()
        self.test_download_file()
        # self.test_go_to_patient()

# Run tests
TestAutoDownloadPdf().run_tests()
