import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from task_automation.auto_download_pdf import AutoDownloadPdf
from task_automation.utils import load_config

script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "..", "..", "config.ini")


def should_skip():
    config = load_config(config_path)
    return config.get("test_auto_download_pdf") not in ("1", "True")


@pytest.mark.skipif(should_skip(), reason="Tests disabled in config")
class TestAutoDownloadPdf:
    dates_path = os.path.join(script_dir, "auto_download_pdf.dates.txt")
    app = AutoDownloadPdf(config_path, dates_path)

    def test_activate_app(self):
        result = self.app.activate_app()
        assert result

    def test_download_file(self):
        result = self.app.download_file()
        assert result

    def test_go_to_report(self):
        result = self.app.go_to_report(self.app.date_entries[0]["fullDate"])
        assert result

    def test_go_to_calendar(self):
        result = self.app.go_to_calendar(self.app.date_entries[0])
        assert result

    def test_go_to_dossier(self):
        result = self.app.go_to_dossier(0, 0)
        assert result
