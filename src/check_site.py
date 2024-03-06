from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display

import os
from typing import List
import shutil

from run_check import run_check, RunCheckTimeoutException
from site_check_config import SiteCheckConfig


# --- glob ---
PROFILE_DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "profile_data")


# --- func ---
def get_driver():
    """
    purpose: create selenium driver
    :return:
    """
    # create virtual display for raspberry pi
    if os.name != "nt":
        print("creating virtual display")
        display = Display(visible=0, size=(800, 600))
        display.start()

    print("creating chrome driver")
    max_attempts = 3
    for attempt in range(max_attempts):
        # attempt to resolve environment issues
        if attempt == 1:
            kill_drivers()
        elif attempt == 2:
            delete_profile_data()

        # create driver
        try:
            options = ChromeOptions()
            options.add_argument(f"--user-data-dir={PROFILE_DATA_FOLDER}")
            print(f"os name: {os.name}")
            if os.name == "nt":  # selenium manager will find driver
                return Chrome()
            else:  # need to use custom driver on raspberry pi
                return Chrome(service=Service(executable_path="/usr/lib/chromium-browser/chromedriver"))
        except Exception as e:
            print(f"failed to create driver due to {type(e)}: {e}")
            if attempt == max_attempts:
                raise e


def kill_drivers():
    print("killing all driver processes")
    if os.name == "nt":
        os.system("taskkill /F /IM chromedriver.exe")
    else:
        os.system("pkill chromedriver")
    print("processes killed")


def delete_profile_data():
    print("deleting profile data")
    shutil.rmtree(PROFILE_DATA_FOLDER)
    print("profile data deleted")


def check_site(scf: SiteCheckConfig):
    result = []
    for attempt in range(scf.max_check_attempts):
        try:
            check_time_sec = int(scf.run_frequency_sec * 0.9 / scf.max_check_attempts)
            result = run_check(check_site_single_attempt, check_time_sec, scf)
        except RunCheckTimeoutException:
            result = ["check exceeded timeout"]
        if not result:
            return result
    return result


def check_site_single_attempt(scf: SiteCheckConfig) -> List[str]:
    """
    purpose: checks if a site is accessible
    :return:
    """
    driver = get_driver()
    driver.implicitly_wait(20)

    print(f"going to {scf.site}")
    driver.get(scf.site)

    print("entering credentials")
    driver.find_element(By.ID, scf.username_id).send_keys(scf.username)
    driver.find_element(By.ID, scf.password_id).send_keys(scf.password + Keys.ENTER)

    print("checking for expected element")
    try:
        driver.find_element(By.ID, scf.expected_element_id)
        print("expected element found")
        driver.quit()
        return []
    except TimeoutException:
        driver.quit()
        return [f"failed to reach {scf.site_name} after login"]
