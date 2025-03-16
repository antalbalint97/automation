#!/usr/bin/env python
# coding: utf-8
import sys
import time
#from datetime import datetime
from datetime import datetime
import pytz  # pip install pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Budapest időzóna beállítása
budapest_tz = pytz.timezone("Europe/Budapest")

# Időbélyeg létrehozása Budapest idő szerint
timestamp = datetime.now(budapest_tz).strftime("%Y-%m-%d-%H-%M-%S")

# --- Read input SERIES-NUMBER pairs from command-line arguments ---
# Example usage: python gepkocsi_betet.py "12:345678" "34:987654"
series_numbers = {}

with open("gepkocsinyeremeny_results.txt", "w", encoding="utf-8") as file:
    pass  # This ensures the file is opened and closed properly.

for arg in sys.argv[1:]:  # Skip the script name
    try:
        series, number = arg.split(":")
        series_numbers[series] = number
    except ValueError:
        print(f"[ERROR] Invalid format: {arg}. Expected format: SERIES:NUMBER")
        sys.exit(1)
# Print dictionary before execution
print("[INFO] Running the script for the following series-number pairs:")
print(series_numbers)

# --- Selenium Setup ---
options = webdriver.ChromeOptions()
# Uncomment this line for automation
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    for SERIES, NUMBER in series_numbers.items():
        LOG_ENTRY = f"[INFO] Processing: Series {SERIES}, Number {NUMBER}"
        print(LOG_ENTRY)

        try:
            driver.get("https://www.otpbank.hu/portal/hu/megtakaritas/forint-betetek/gepkocsinyeremeny")
            time.sleep(3)  # Allow the page to load

            # --- Handle Cookie Pop-up ---
            LOG_ENTRY = "[INFO] Checking for cookie pop-up..."
            print(LOG_ENTRY)
            try:
                cookie_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "gdrp-btn__submit"))
                )
                cookie_button.click()
                time.sleep(2)
                LOG_ENTRY = "[INFO] Cookies accepted."
                print(LOG_ENTRY)
            except Exception as e:
                LOG_ENTRY = "[INFO] No cookie pop-up found, continuing...Exception: {e}"
                print(LOG_ENTRY)

            # --- Wait for Form Elements ---
            LOG_ENTRY = "[INFO] Waiting for form elements to load..."
            print(LOG_ENTRY)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "car-sweepstakes-series")))
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "car-sweepstakes-number")))

            # Locate input fields
            LOG_ENTRY = "[INFO] Locating input fields..."
            print(LOG_ENTRY)
            series_input = driver.find_element(By.ID, "car-sweepstakes-series")
            number_input = driver.find_element(By.ID, "car-sweepstakes-number")

            # Ensure elements are interactable
            LOG_ENTRY = "[INFO] Checking if input fields are interactable..."
            print(LOG_ENTRY)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "car-sweepstakes-series")))

            # --- Enter Values Properly ---
            LOG_ENTRY = f"[INFO] Entering values: {SERIES} - {NUMBER}"
            print(LOG_ENTRY)

            series_input.click()
            time.sleep(0.5)
            series_input.send_keys(SERIES)

            number_input.click()
            time.sleep(0.5)
            number_input.send_keys(NUMBER)

            time.sleep(2)  # Small pause to let the UI register inputs

            # --- Click the "Ellenőrzöm" Button ---
            LOG_ENTRY = "[INFO] Clicking the 'Ellenőrzöm' button..."
            print(LOG_ENTRY)
            check_button = driver.find_element(By.ID, "car-sweepstakes-form-btn")
            check_button.click()

            # --- Wait for the Result ---
            LOG_ENTRY = "[INFO] Waiting for the result..."
            print(LOG_ENTRY)
            try:
                result_element = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "car-sweepstakes-widget__title"))
                )
                result_text = result_element.text
            except Exception as e:
                result_text = "No result found. {e}"

            # --- Generate Timestamp ---
            #timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            #budapest_tz = pytz.timezone("Europe/Budapest")
            timestamp = datetime.now(budapest_tz).strftime("%Y-%m-%d-%H-%M-%S")

            # --- Save & Print Result ---
            LOG_ENTRY = f"{timestamp}: {SERIES}-{NUMBER} {result_text}"
            print(LOG_ENTRY)

            with open("gepkocsinyeremeny_results.txt", "a", encoding="utf-8") as file:
                file.write(LOG_ENTRY + "\n")

        except Exception as e:
            # If any error occurs, log the last successful step and the error message
            #timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            #budapest_tz = pytz.timezone("Europe/Budapest")
            timestamp = datetime.now(budapest_tz).strftime("%Y-%m-%d-%H-%M-%S")
            error_msg = f"{timestamp} [ERROR] Last step: {LOG_ENTRY}\n[ERROR] {str(e)}\n"
            print(error_msg)

            with open("gepkocsinyeremeny_results.txt", "a", encoding="utf-8") as file:
                file.write(error_msg + "\n")

except Exception as e:
    print(f"[FATAL ERROR] Script crashed: {e}")
finally:
    driver.quit()

