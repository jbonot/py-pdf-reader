import re
from datetime import datetime
from enum import Enum

from data_extractor.config import config
from data_extractor.fuzzy_compare import contains, starts_with


def get_config_value(key):
    if "Document" in config and key in config["Document"]:
        return [item.strip().title() for item in config["Document"][key].split(",")]
    return []


supervisors = get_config_value("supervisors")
bodyparts = {}
bodyparts["Knie"] = get_config_value("keywords_knee")
bodyparts["Schouder"] = get_config_value("keywords_shoulder")
bodyparts["Elleboog"] = get_config_value("keywords_elbow")
bodyparts["Pols/hand"] = get_config_value("keywords_hand")
bodyparts["Voet"] = get_config_value("keywords_foot")

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


def get_bodypart(procedure):
    for key, value in bodyparts.items():
        for keyword in value:
            if contains(procedure, keyword):
                return key
    return None


def get_first_nonempty_line(lines, start_index):
    while start_index < len(lines):
        line = lines[start_index].strip()
        if line:
            return line

        start_index += 1


def parse_name_list(lines, start_index):
    def clean_name(full_name, bullet_points):
        # Format: <bullet point> <title> <last name> <first name>
        pattern = rf"^[{"".join(bullet_points)}]*\s*(\S+\.)?\s*(.*)\s+(\S+)$"
        match = re.match(pattern, full_name)
        if match:
            # Return last name
            return match.group(2).title()
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

    # Special case:
    # "Ingreep" is poorly parsed by OCR. Parse the line that comes after "Algemeen"
    if starts_with(line, "Algemeen") and not result[COLUMN.PROCEDURE.value]:
        procedure_line = get_first_nonempty_line(lines, index + 1)
        return COLUMN.PROCEDURE.value, extract_value(procedure_line)

    if starts_with(line, "Lateraliteit") and not result[COLUMN.SIDE.value]:
        col, value = COLUMN.SIDE.value, extract_value(line).lower()
        if starts_with(value, "links"):
            return col, "links"
        if starts_with(value, "rechts"):
            return col, "rechts"
        return col, value

    if starts_with(line, "Chirugen") and not result[COLUMN.SUPERVISOR.value]:
        surgeons = parse_name_list(lines, index + 1)
        for index, surgeon in enumerate(surgeons):
            for name in supervisors:
                if starts_with(surgeon, name):
                    surgeons[index] = name.title()
                    break

        return COLUMN.SUPERVISOR.value, ",".join(surgeons)

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
        if cell is COLUMN.PROCEDURE.value:
            bodypart = get_bodypart(value)
            if bodypart:
                result[COLUMN.JOINT.value] = bodypart
        result[cell] = value

    if debug:
        return str(result)

    excel_line = "\t".join(result.get(column.value, "") for column in order)
    return excel_line
