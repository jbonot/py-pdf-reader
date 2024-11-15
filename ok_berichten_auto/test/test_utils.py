import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import ok_berichten_auto.utils as utils


class TestUtils:
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.ini")
    dates_path = os.path.join(os.path.dirname(__file__), "auto_download_pdf.dates.txt")

    def test_capitalize_name(self):
        cases = [
            ["JOHN DOE", "John Doe"],
            ["john doe", "John Doe"],
        ]
        for input_name, expected in cases:
            result = utils.capitalize_name(input_name)
            assert result == expected

    def test_load_config(self):
        config = utils.load_config(self.config_path)
        assert "windowTitle" in config
        assert len(config.get("windowTitle").strip()) > 0

    def test_get_person_data(self):
        cases = [
            [
                "24j (01/01/2000) DOE, JANE (NL)",
                {"age": "24j", "dob": "01.01.2000", "name": "Doe, Jane", "lang": "NL"},
            ],
            ["invalid", None],
        ]

        for input_text, expected_data in cases:
            result = utils.get_person_data(input_text)
            if result:
                assert result["age"] == expected_data["age"]
                assert result["dob"] == expected_data["dob"]
                assert result["name"] == expected_data["name"]
            else:
                assert result == expected_data

    def test_load_dates(self):
        expected = [
            {
                "fullDate": "03/05/2024",
                "day": "03",
                "month": "05",
                "year": "2024",
                "name": "Skywalker",
            },
            {
                "fullDate": "04/05/2024",
                "day": "04",
                "month": "05",
                "year": "2024",
                "name": "Solo",
            },
        ]
        date_entries = utils.load_dates(self.dates_path)

        for index, entry in enumerate(date_entries):
            expected_entry = expected[index]
            assert entry["day"] == expected_entry["day"]
            assert entry["month"] == expected_entry["month"]
            assert entry["year"] == expected_entry["year"]
            assert entry["name"] == expected_entry["name"]
