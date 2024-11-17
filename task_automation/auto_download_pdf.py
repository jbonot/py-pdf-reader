import time

import ocrhelper
import pyautogui as pag
from lxml import etree
from pywinauto import Application
from pywinauto.findwindows import find_windows

import task_automation.utils as utils

tesseract_params = {"lang": "nld+fra"}


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

            for x, y in ocrhelper.locate_text_at_position(
                entry["name"], should_process=True, tesseract_params=tesseract_params
            ):
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
        # To-do: check bbox
        tree_hocr = ocrhelper.get_hocr_from_bbox(
            [28, 296, 235, 2024],
            should_process=True,
            tesseract_params=tesseract_params,
        )

        elements = etree.fromstring(tree_hocr, etree.HTMLParser()).xpath(
            '//*[contains(text(), "Orthopedie")]'
        )

        if not elements:
            print("No element with text 'Orthopedie' found.")
            return 0

        title_attr = elements[0].get("title")

        if not title_attr or "bbox" not in title_attr:
            print("BBox not found in the title attribute.")
            return 0

        bbox = title_attr.split("bbox")[-1].split(";")[0].strip()
        bbox_coords = list(map(int, bbox.split()))
        center_x = (bbox_coords[0] + bbox_coords[2]) / 2
        center_y = (bbox_coords[1] + bbox_coords[3]) / 2

        # To-Do: Check if double-click is possible, or if need to click on node
        pag.doubleClick(center_x, center_y)

        # To-do: Check accuracy
        pag.sleep(0.5)
        pag.doubleClick(center_x, center_y + 32)

        return 1

    def download_file(
        self,
    ):
        file_name = ""
        text = ocrhelper.read_text_in_bbox(
            [257, 51, 644, 73], tesseract_params=tesseract_params
        )
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
            text = ocrhelper.read_text_at_position(
                [1093, 603, 1222, 627], tesseract_params=tesseract_params
            )
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
