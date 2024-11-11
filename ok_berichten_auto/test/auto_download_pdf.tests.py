import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ok_berichten_auto.auto_download_pdf import AutoDownloadPdf

# Sample class for handling test cases and functions
class TestAutoDownloadPdf:

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        config_path = os.path.join(script_dir, '..', '..', 'config.ini')
        dates_path = os.path.join(script_dir, 'auto_download_pdf.dates.txt')
        self.app = AutoDownloadPdf(config_path, dates_path)


    def assert_test(self, result, test):
        """Custom assert function for test results"""
        if result:
            print(f"Pass\t{test}")
        else:
            print(f"Fail\t{test}")

    def test_activate_app(self):
        """Test ActivateApp function"""
        result = self.app.activate_app()
        self.assert_test(result, 'TestActivateApp')

    def test_download_file(self):
        """Test DownloadFile function"""
        result = self.app.download_file()
        self.assert_test(result, 'TestDownloadFile')

    def test_go_to_report(self):
        """Test GoToReport function"""
        result = self.app.go_to_report(self.app.date_entries[0]['fullDate'])  # Use the first entry for testing
        self.assert_test(result, 'TestGoToReport')

    def test_go_to_calendar(self):
        """Test GoToCalendar function"""
        result = self.app.go_to_calendar(self.app.date_entries[0])  # Use the first entry for testing
        self.assert_test(result, 'TestGoToCalendar')

    def test_go_to_dossier(self):
        """Test GoToPatient function"""
        result = self.app.go_to_dossier(0, 0) 
        self.assert_test(result, 'TestGoToDossier')

    def run_tests(self):
        """Run all tests"""
        self.test_activate_app()

        # Success
        self.test_go_to_calendar()
        # self.test_download_file()

        # To-do
        # self.test_go_to_report()
        # self.test_go_to_patient()

# Run tests
TestAutoDownloadPdf().run_tests()
