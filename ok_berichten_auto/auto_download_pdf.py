import pyautogui as pag
import time
from pywinauto import Application

from ok_berichten_auto.utils import get_patient_data, load_config, load_dates, locate_text_at_position

# Ensure you have installed required packages:
# pip install pyautogui pytesseract pywinauto

def download_all_entries():
    processed = []
    dates = load_dates('dates.txt')
    for entry in dates:
        go_to_calendar(entry)
        
        for coord in locate_text_at_position(entry['name']):
            pag.rightClick(coord['x'], coord['y'])
            go_to_patient(coord['x'], coord['y'])
            go_to_report(entry['fullDate'])
            download_file()
            
            # To-do: Go back to calendar view
            go_to_calendar(entry)

def activate_or_exit(title):
    try:
        app = Application().connect(title=title)
        app_window = app[title]
        app_window.set_focus()
    except Exception:
        print(f"Could not find window: {title}")
        exit()

def go_to_patient(start_x, start_y):
    pag.click(start_x + 20, start_y + 5)  # "Selecteer patiënt" adjustment
    # Additional clicks can be added here as required
    # To-do: Save name via OCR before proceeding

def go_to_calendar(entry):
    pag.click(283, 33)  # "Afspraken"
    time.sleep(0.5)
    pag.click(360, 140)  # "Overzicht OK andere dag"
    time.sleep(0.5)

    activate_or_exit("Selecteer een datum")

    # Enter day, month, and year
    pag.typewrite(entry['day'])
    time.sleep(0.5)
    pag.typewrite(entry['month'])
    time.sleep(0.5)
    pag.typewrite(entry['year'])
    time.sleep(0.5)
    pag.press('tab')
    pag.press('space')

def go_to_report(date):
    # Click necessary elements for navigating to the report
    # Implementation depends on the exact GUI layout
    return 0

def download_file():
    file_name = ""
    patient = get_patient_data(r"(<age>) (DD/MM/YYY) Last Name, First Name (<lang>)")
    if patient:
        file_name = f"{patient['name']} {patient['dob']}"

    # Click "Afdrukken" (print)
    # Click "Nota view" (note view)
    time.sleep(1)
    activate_or_exit("Print")
    
    if file_name:
        pag.typewrite(file_name)
        pag.press('tab')
        pag.press('enter')  # "Opslaan" (Save)
    else:
        print("Patient info not found")
        return 0

    return 1

def activate_app(filename):
    config = load_config(filename)
    if 'windowTitle' not in config:
        print("Missing config: windowTitle")
        exit()

    title = config['windowTitle']
    try:
        app = Application().connect(title=title)
        app.window(title=title).set_focus()
        return 1
    except Exception:
        print(f"Window not found: {title}")
        exit()