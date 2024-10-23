import re
from datetime import datetime
from enum import Enum

from data_extractor.fuzzy_compare import starts_with

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
    COLUMN.MATERIAL_COMPANY,
]


def parse_name_list(lines, start_index):
    def clean_name(full_name, bullet_points):
        # Format: <bullet point> <title> <last name> <first name>
        pattern = rf"^[{"".join(bullet_points)}]*\s*(\S+\.)?\s*(.*)\s+(\S+)$"
        match = re.match(pattern, full_name)
        if match:
            # Return last name
            return match.group(2)
        else:
            return None

    names = []
    bullet_points = ("-", "~")
    while start_index < len(lines):
        line = lines[start_index].strip()

        if not line:
            start_index += 1
            continue

        if line.startswith(bullet_points):
            names.append(clean_name(line, bullet_points))
            start_index += 1
        else:
            break

    return names


def parse_line(line, lines, index, result):
    def extract_value(line):
        # Define a regex pattern with the delimiters
        pattern = r"[:;,]\s*(.*)"
        match = re.search(pattern, line)

        if match:
            return match.group(1).strip()

        # Return the entire line
        return line.strip()

    match = re.search(date_pattern, line)
    if match and not result[COLUMN.SURGERY_DATE.value]:
        return COLUMN.SURGERY_DATE.value, match.group(1)

    if starts_with(line, "Ingreep", 0.55) and not result[COLUMN.PROCEDURE.value]:
        return COLUMN.PROCEDURE.value, extract_value(line)

    if starts_with(line, "Lateraliteit") and not result[COLUMN.SIDE.value]:
        col, value = COLUMN.SIDE.value, extract_value(line).lower()
        if starts_with(value, "links"):
            return col, "links"
        if starts_with(value, "rechts"):
            return col, "rechts"
        return col, value

    if starts_with(line, "Chirugen") and not result[COLUMN.SUPERVISOR.value]:
        chirugen = parse_name_list(lines, index + 1)
        return COLUMN.SUPERVISOR.value, ",".join(chirugen)

    return None, None


def parse_doc(filename, text, debug=False):
    result = {column.value: "" for column in order}

    # Format: <last name>, <first name>, <dob>
    pattern = r"^(.*?),\s*(.*?)\s+(\d{2}\.\d{2}\.\d{4})$"
    match = re.match(pattern, filename)

    if match:
        last_name = match.group(1).rstrip(",")
        first_name = match.group(2)
        dob = datetime.strptime(match.group(3), "%d.%m.%Y").strftime("%d/%m/%Y")

        result[COLUMN.LAST_NAME.value] = last_name
        result[COLUMN.FIRST_NAME.value] = first_name
        result[COLUMN.DOB.value] = dob

    lines = text.splitlines()
    for index, line in enumerate(lines):
        cell, value = parse_line(line.strip(), lines, index, result)
        if cell is None:
            continue
        result[cell] = value

    if debug:
        return str(result)

    excel_line = "\t".join(result.get(column.value, "") for column in order)
    return excel_line
