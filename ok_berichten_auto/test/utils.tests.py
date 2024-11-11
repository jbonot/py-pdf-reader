import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import ok_berichten_auto.utils as utils

script_dir = os.path.dirname(__file__)

class TestUtils:
    config_path = os.path.join(script_dir, '..', '..', 'config.ini')
    dates_path = os.path.join(script_dir, 'auto_download_pdf.dates.txt')

    def __init__(self):
        self.config = utils.load_config(self.config_path)
        self.date_entries = utils.load_dates(self.dates_path)

    def assert_test(self, result, key, test):
        """Custom assertion method for tests"""
        if result:
            print(f"Pass\t{key}\t{test}")
        else:
            print(f"Fail\t{key}\t{test}")

    def test_capitalize_name(self):
        """Test capitalize_name function"""
        cases = [
            ["JOHN DOE", "John Doe"],
            ["john doe", "John Doe"],
        ]
        for index, (input_name, expected) in enumerate(cases):
            result = utils.capitalize_name(input_name)
            self.assert_test(result == expected, index, "TestCapitalizeName")

    def test_load_config(self):
        """Test load_config function"""
        self.assert_test("windowTitle" in self.config, "key", "TestLoadConfig")
        self.assert_test(len(self.config.get("windowTitle").strip()) > 0, "value", "TestLoadConfig")


    def test_get_patient_data(self):
        """Test get_patient_data function"""
        cases = [
            ["24j (01/01/2000) DOE, JANE (NL)", {
                "age": "24j",
                "dob": "01.01.2000",
                "name": "Doe, Jane",
                "lang": "NL"
            }],
            ["invalid", None],
        ]
        
        for index, (input_text, expected_data) in enumerate(cases):
            result = utils.get_patient_data(input_text)
            if result:
                self.assert_test(
                    result['age'] == expected_data['age'] and
                    result['dob'] == expected_data['dob'] and
                    result['name'] == expected_data['name'],
                    index, "TestGetPatientData"
                )
            else:
                self.assert_test(result == expected_data, index, "TestGetPatientData")

    def test_load_dates(self):
        """Test load_dates function"""
        expected = [
            {"fullDate": "03/05/2024", "day": "03", "month": "05", "year": "2024", "name": "Skywalker"},
            {"fullDate": "04/05/2024", "day": "04", "month": "05", "year": "2024", "name": "Solo"}
        ]
        
        for index, entry in enumerate(self.date_entries):
            expected_entry = expected[index]
            self.assert_test(
                entry['day'] == expected_entry['day'] and
                entry['month'] == expected_entry['month'] and
                entry['year'] == expected_entry['year'] and
                entry['name'] == expected_entry['name'],
                index, "TestLoadDates"
            )

    def test(self):
        """Run all tests"""
        self.test_capitalize_name()
        self.test_load_config()
        self.test_get_patient_data()
        self.test_load_dates()

TestUtils().test()
