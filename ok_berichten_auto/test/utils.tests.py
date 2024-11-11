from ok_berichten_auto.utils import capitalize_name, get_hocr_content, get_patient_data, load_config, load_dates

class TestUtils:
    def __init__(self):
        pass

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
            result = capitalize_name(input_name)
            self.assert_test(result == expected, index, "TestCapitalizeName")

    def test_load_config(self):
        """Test load_config function"""
        config = load_config('../config.example.ini')
        self.assert_test("windowTitle" in config, "key", "TestLoadConfig")
        self.assert_test(config.get("windowTitle") == "Editor", "value", "TestLoadConfig")


    def test_get_patient_data(self):
        """Test get_patient_data function"""
        cases = [
            ["24j (01/01/2000) DOE, JANE (NL)", {
                "age": "24j",
                "dob": "01.01.2000",
                "name": "Doe, Jane",
                "country": "NL"
            }],
            ["invalid", None],
        ]
        
        for index, (input_text, expected_data) in enumerate(cases):
            result = get_patient_data(input_text)
            if result:
                self.assert_test(
                    result['age'] == expected_data['age'] and
                    result['dob'] == expected_data['dob'] and
                    result['name'] == expected_data['name'] and
                    result['country'] == expected_data['country'],
                    index, "TestGetPatientData"
                )
            else:
                self.assert_test(result == expected_data, index, "TestGetPatientData")


    def test_get_hocr_content(self):
        """Test get_hocr_content function"""
        application_bounding_box = {'x': 0, 'y': 74, 'width': 2560, 'height': 1326}
        config = load_config('../config.ini')
        if 'windowTitle' in config:
            get_hocr_content(application_bounding_box)
        else:
            print("Window Title missing in config.")

    def test_load_dates(self):
        """Test load_dates function"""
        expected = [
            {"fullDate": "03/05/2024", "day": "03", "month": "05", "year": "2024", "name": "Skywalker"},
            {"fullDate": "04/05/2024", "day": "04", "month": "05", "year": "2024", "name": "Solo"}
        ]
        entries = load_dates('../dates.example.txt')
        for index, entry in enumerate(entries):
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
        self.test_get_hocr_content()

TestUtils().test()
