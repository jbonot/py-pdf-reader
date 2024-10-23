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
    def clean_name(full_name, delimiter):
        parts = full_name.strip().replace(delimiter, "").split()

        # If the first part is a title, remove it
        if parts[0].endswith("."):
            parts = parts[1:]

        # Join all but the last part (which is assumed to be the first name)
        # as the last name
        return " ".join(parts[:-1]).title()

    names = []
    delimiters = ["-", "~"]
    while start_index < len(lines):
        line = lines[start_index].strip()

        if not line:
            start_index += 1
            continue

        for delimiter in delimiters:
            if delimiter in line:
                names.append(clean_name(line, delimiter))
                start_index += 1
                break
        else:
            break

    return names


def parse_line(line, lines, index):
    def extract_value(line):
        # Define a list of delimiters
        delimiters = [":", ";", ","]
        # Find the first occurrence of any delimiter
        for delimiter in delimiters:
            if delimiter in line:
                return line.split(delimiter, 1)[1].strip()

        # Return the original line if no delimiter was found
        return line.strip()

    match = re.search(date_pattern, line)
    if match:
        return COLUMN.SURGERY_DATE.value, match.group(1)

    if starts_with(line, "Ingreep", 0.55):
        return COLUMN.PROCEDURE.value, extract_value(line)

    if starts_with(line, "Lateraliteit"):
        col, value = COLUMN.SIDE.value, extract_value(line).lower()
        if starts_with(value, "links"):
            return col, "links"
        if starts_with(value, "rechts"):
            return col, "rechts"
        return col, value

    if starts_with(line, "Chirugen"):
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
        cell, value = parse_line(line.strip(), lines, index)
        if cell is None:
            continue
        result[cell] = value

    if debug:
        return str(result)

    excel_line = "\t".join(result.get(column.value, "") for column in order)
    return excel_line
