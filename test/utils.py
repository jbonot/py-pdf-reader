import os

from task_automation.utils import load_config

script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, "..", "config.ini")
config = load_config(config_path)


def should_skip(flag):
    return config.get("test_auto_download_pdf") not in ("1", "True")
