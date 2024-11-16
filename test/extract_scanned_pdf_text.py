import os
import sys
from pathlib import Path

import Levenshtein

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data_extractor.extract_scanned_pdf_text import extract_text_from_pdf

data_path = os.path.join(Path(__file__).parent, "data")

results = []
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

    results.append(
        {
            "distance": Levenshtein.distance(extracted_text, transcript),
            "accuracy": Levenshtein.ratio(extracted_text, transcript),
        }
    )

if not len(results):
    print("No test data")
    exit

# Calculate averages
avg_distance = sum(result["distance"] for result in results) / len(results)
avg_accuracy = sum(result["accuracy"] for result in results) / len(results) * 100

# Print header
print(f"| {'':<3} | {'DISTANCE':<9} | {'ACCURACY':<8} |")
print("-" * 36)

# Print results
for i, result in enumerate(results, start=1):
    print(f"| {i:<3} | {result['distance']:<9} | {result['accuracy']*100:<7.2f}% |")

# Print average
print("-" * 36)
print(f"| AVG | {int(avg_distance):<9} | {avg_accuracy:<7.2f}% |")
