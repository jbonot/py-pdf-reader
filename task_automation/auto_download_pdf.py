import time

import pyautogui as pag
from pywinauto import Application
from pywinauto.findwindows import find_windows

import task_automation.utils as utils


class AutoDownloadPdf:
    def __init__(self, config_path, dates_path):
        self.config = utils.load_config(config_path)
        self.date_entries = utils.load_dates(dates_path)

        if (
            "pdfDestination" in self.config
            and len(self.config["pdfDestination"].strip()) > 1
        ):
            self.pdf_destination = self.config["pdfDestination"]
            self.is_file_destination_set = False

    def download_all_entries(self):
        for entry in self.date_entries:
            self.go_to_calendar(entry)

            for x, y in utils.locate_text_at_position(entry["name"]):
                self.go_to_dossier(x, y)
                self.go_to_report(entry["fullDate"])
                self.download_file()

    def activate_or_exit(self, title):
        windows = find_windows(title_re=f"^{title}")
        if windows:
            app = Application().connect(handle=windows[0])
            app.window(handle=windows[0]).set_focus()
            return 1
        else:
            print(f"Window not found: {title}")
            exit()

    def go_to_dossier(self, start_x, start_y):
        pag.rightClick(start_x, start_y)
        pag.click(start_x + 90, start_y + 32)
        pag.press("f6")

    def go_to_calendar(self, entry):
        pag.click(283, 33)  # "Afspraken"
        time.sleep(0.5)
        pag.click(360, 140)  # "Overzicht OK andere dag"
        time.sleep(1)

        self.activate_or_exit("Selecteer een datum")

        # Enter day, month, and year
        pag.typewrite(entry["day"])
        pag.sleep(0.1)
        pag.typewrite(entry["month"])
        pag.sleep(0.1)
        pag.typewrite(entry["year"])

        pag.click(1338, 786)
        pag.sleep(3)
        return 1

    def go_to_report(self, date):
        # Click necessary elements for navigating to the report
        # Implementation depends on the exact GUI layout
        return 0

    def download_file(
        self,
    ):
        file_name = ""
        text = utils.read_text_at_position([257, 51, 644, 73])
        person = utils.get_person_data(text)
        if person:
            file_name = f"{person['name']} {person['dob']}"

        pag.click(597, 124)  # "Afdrukken"
        pag.click(627, 235)  # "Nota view"
        time.sleep(3)
        pag.click(1430, 833)
        time.sleep(1)

        if file_name:
            if self.pdf_destination and not self.is_file_destination_set:
                # Set destination
                pag.hotkey("alt", "d")
                pag.typewrite(self.config["pdfDestination"])
                pag.press("enter")

                for _ in range(6):
                    pag.press("tab")

                time.sleep(3)

            pag.typewrite(file_name)
            pag.press("enter")  # "Opslaan" (Save)
            time.sleep(1)

            # If the file exists, cancel saving
            text = utils.read_text_at_position([1093, 603, 1222, 627])
            if text.strip() == "Opslaan als bevestigen":
                pag.press("enter")  # "Nee"
                pag.press("esc")
            else:
                self.is_file_destination_set = True

            print("Done:", file_name)
            pag.click(2543, 91)  # Close dossier

        else:
            print("Person info not found")
            return 0

        return 1

    def activate_app(self):
        if "windowTitle" not in self.config:
            print("Missing config: windowTitle")
            exit()

        self.activate_or_exit(self.config["windowTitle"])
