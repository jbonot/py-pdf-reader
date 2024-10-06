from enum import Enum
from datetime import datetime
import re

date_pattern = r"\b(\d{1,2}/\d{1,2}/\d{4})\b"

class COLUMN(Enum):
    LAST_NAME = "naam"
    FIRST_NAME = "voornaam"
    GENDER = "geslacht"
    DOB = "geboortedatum"
    SURGERY_DATE = "datum_ingreep"
    JOINT = "gewricht"
    PROCEDURE = "ingreep"
    SIDE = "zijde"
    SUPERVISOR = "supervisor"
    SURGEON_ASSISTANT = "chirug_asssistent"
    MATERIAL_COMPANY = "firma_material"

order = [
    COLUMN.LAST_NAME,
    COLUMN.FIRST_NAME,
    COLUMN.GENDER,
    COLUMN.DOB,
    COLUMN.SURGERY_DATE,
    COLUMN.JOINT,
    COLUMN.PROCEDURE,
    COLUMN.SIDE,
    COLUMN.SUPERVISOR,
    COLUMN.SURGEON_ASSISTANT,
    COLUMN.MATERIAL_COMPANY
]

def parse_name_list(lines, start_index):
    def clean_name(full_name):
        # Remove the dash and extra spaces
        parts = full_name.strip().replace("-", "").split()

        # If the first part is a title, remove it
        if parts[0].endswith('.'):
            parts = parts[1:]

        # Join all but the last part (which is assumed to be the first name) as the last name
        return " ".join(parts[:-1]).title()

    names = []
    while start_index < len(lines) and lines[start_index].strip().startswith("-"):
        full_name = lines[start_index].strip()  # Strip once for efficiency
        last_name = clean_name(full_name)
        names.append(last_name)
        start_index += 1

    return names

def parse_line(line, lines, index):
    def extract_value(line):
        return line.split(":", 1)[1].strip()

    match = re.search(date_pattern, line)
    if match:
        return COLUMN.SURGERY_DATE.value, match.group(1)
    
    if line.startswith("Ingreep"):
        return COLUMN.PROCEDURE.value, extract_value(line)
    
    if line.startswith("Lateraliteit"):
        return COLUMN.SIDE.value, extract_value(line).lower()
    
    if line.startswith("Chirugen"):
        chirugen = parse_name_list(lines, index + 1)
        return COLUMN.SUPERVISOR.value, ",".join(chirugen)
    
    return None, None


def parse_doc(filename, text, debug):
    result = {column.value: "" for column in order}
    parts = filename.split()
    result[COLUMN.LAST_NAME.value] = parts[0].rstrip(',')
    result[COLUMN.FIRST_NAME.value] = parts[1]
    result[COLUMN.DOB.value] = datetime.strptime(parts[2], "%d.%m.%Y").strftime("%d/%m/%Y")

    lines = text.splitlines()
    for index, line in enumerate(lines):
        cell, value = parse_line(line.strip(), lines, index)
        if cell is None:
            continue
        result[cell] = value
    
    if (debug):
        return str(result)
        
    excel_line = "\t".join(result.get(column.value, "") for column in order)
    return excel_line