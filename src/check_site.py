from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from run_check import run_check, RunCheckTimeoutException

import os
from typing import List
import shutil


# --- glob ---
PROFILE_DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "profile_data")


# --- func ---
def get_driver():
    """
    purpose: create selenium driver
    :return:
    """
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
            return Chrome()
        except Exception as e:
            print(f"failed to create driver due to {type(e)}: {e}")
            if attempt == max_attempts:
                raise e


def kill_drivers():
    print("killing all driver processes")
    os.system("taskkill /F /IM chromedriver.exe")
    print("processes killed")


def delete_profile_data():
    print("deleting profile data")
    shutil.rmtree(PROFILE_DATA_FOLDER)
    print("profile data deleted")


def check_site(site: str, username_locator: (By, str), password_locator: (By, str), expected_element_locator: (By, str)):
    max_attempts: int = 3
    result = []
    for attempt in range(max_attempts):
        try:
            result = run_check(check_site_single_attempt, 2 * 60, site, username_locator, password_locator, expected_element_locator)
        except RunCheckTimeoutException:
            result = ["check exceeded timeout"]
        if not result:
            return result
    return result


def check_site_single_attempt(site: str, username_locator: (By, str), password_locator: (By, str), expected_element_locator: (By, str)) -> List[str]:
    """
    purpose: checks if a site is accessible
    :return:
    """
    print("creating driver")
    driver = get_driver()
    driver.implicitly_wait(20)

    print(f"going to {site}")
    driver.get(site)

    print("entering credentials")
    driver.find_element(By.ID, "emailInput").send_keys(os.environ["USERNAME"])
    driver.find_element(By.ID, "passwordInput").send_keys(os.environ["PASSWORD"] + Keys.ENTER)

    print("checking for expected element")
    try:
        driver.find_element(*expected_element_locator)
        print("expected element found")
        driver.quit()
        return []
    except TimeoutException:
        driver.quit()
        return [f"failed to reach {site} after login"]
