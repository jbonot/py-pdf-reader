import pyautogui as pag
import time
from pywinauto import Application
from pywinauto.findwindows import find_windows

from ok_berichten_auto.utils import get_patient_data, load_config, load_dates, locate_text_at_position, read_text_at_position

# Ensure you have installed required packages:
# pip install pyautogui pytesseract pywinauto

def download_all_entries():
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
    text = read_text_at_position([257,51, 644, 73])
    patient = get_patient_data(text)
    if patient:
        file_name = f"{patient['name']} {patient['dob']}"
        
    pag.click(597, 124)  # "Afdrukken"
    pag.click(627, 235)  # "Nota view"
    time.sleep(3)
    pag.click(1430, 833)
    time.sleep(1)
    
    
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
    windows = find_windows(title_re=f"^{title}")
    if windows:
        app = Application().connect(handle=windows[0])
        app.window(handle=windows[0]).set_focus()
        return 1
    else:
        print(f"Window not found: {title}")
        exit()