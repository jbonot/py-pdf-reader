import os
import sys
from pathlib import Path

import Levenshtein
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import utils as test_utils

from data_extractor.extract_scanned_pdf_text import extract_text_from_pdf

data_path = os.path.join(Path(__file__).parent, "data")


@pytest.mark.skipif(
    test_utils.should_skip("test_extract_scanned_pdf"),
    reason="Tests disabled in config",
)
def test_accuracy():
    assert os.path.isdir(data_path)
    test_cases = os.listdir(data_path)
    assert len(test_cases) > 0
    for case in test_cases:
        case_path = os.path.join(data_path, case)
        if os.path.isfile(case_path):
            continue

        pdf = next(
            (file for file in os.listdir(case_path) if file.lower().endswith(".pdf")),
            None,
        )
        assert pdf

        txt = next(
            (file for file in os.listdir(case_path) if file.lower().endswith(".txt")),
            None,
        )
        assert txt

        with open(os.path.join(data_path, case, txt), "r") as file:
            transcript = file.read()

        with open(os.path.join(data_path, case, pdf), "rb") as pdf_file:
            extracted_text = extract_text_from_pdf(pdf_file)

        assert Levenshtein.ratio(extracted_text, transcript) > 0.9
