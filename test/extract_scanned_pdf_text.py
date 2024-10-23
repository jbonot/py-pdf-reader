import os
import sys
from pathlib import Path

import Levenshtein

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_extractor.extract_scanned_pdf_text import extract_text_from_pdf

data_path = os.path.join(Path(__file__).parent, "data")

print("CASE\tDISTANCE\tACCURACY")
print("---------------------------------")
for case in os.listdir(data_path):
    case_path = os.path.join(data_path, case)
    if os.path.isfile(case_path):
        continue

    pdf = next(
        (file for file in os.listdir(case_path) if file.lower().endswith(".pdf")),
        None,
    )
    if not pdf:
        print("PDF not found")
        continue

    txt = next(
        (file for file in os.listdir(case_path) if file.lower().endswith(".txt")),
        None,
    )
    if not txt:
        print("Transcript .txt not found")
        continue

    with open(os.path.join(data_path, case, txt), "r") as file:
        transcript = file.read()

    with open(os.path.join(data_path, case, pdf), "rb") as pdf_file:
        extracted_text = extract_text_from_pdf(pdf_file)

    distance = Levenshtein.distance(extracted_text, transcript)
    accuracy = round(Levenshtein.ratio(extracted_text, transcript) * 100, 2)
    print(f"{case}\t{distance}\t{accuracy}%")
