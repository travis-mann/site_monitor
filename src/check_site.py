import os
import logging
import traceback
from typing import List
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from os_selenium_handler import OSSeleniumHandler, get_os_selenium_handler
from run_check import run_check, RunCheckTimeoutException
from site_check_config import SiteCheckConfig

SCREENSHOT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")


def take_screenshot(driver: WebDriver) -> None:
    if not os.path.exists(SCREENSHOT_FOLDER):
        logging.info(f"creating screenshot directory {SCREENSHOT_FOLDER}")
        os.makedirs(SCREENSHOT_FOLDER)
        logging.info(f"directory created")
    screenshot_name = datetime.now().strftime("%Y_%m_%dT%H_%M_%S-site_screenshot.png")
    full_screenshot_path = os.path.join(SCREENSHOT_FOLDER, screenshot_name)
    logging.info(f"saving screenshot to {full_screenshot_path}")
    driver.save_screenshot(full_screenshot_path)
    logging.info(f"screenshot saved")


def goto_site(driver: WebDriver, scf: SiteCheckConfig, failures: List[str]) -> None:
    logging.info(f"going to {scf.site}")
    try:
        driver.get(scf.site)
    except TimeoutException as e:
        logging.warning(f"failed to get to site due to {type(e)}: {e}\n{traceback.format_exc()}")
        failures.append("failed to get to site")


def enter_credentials_on_site(driver: WebDriver, scf: SiteCheckConfig, failures: List[str]) -> None:
    logging.info("entering credentials")
    try:
        driver.find_element(By.ID, scf.username_id).send_keys(scf.username)
        driver.find_element(By.ID, scf.password_id).send_keys(scf.password + Keys.ENTER)
    except (TimeoutException, NoSuchElementException) as e:
        logging.warning(f"failed to enter credentials due to {type(e)}: {e}\n{traceback.format_exc()}")
        failures.append("failed to enter credentials")


def find_expected_element(driver: WebDriver, scf: SiteCheckConfig, failures: List[str]) -> None:
    logging.info("checking for expected element")
    try:
        driver.find_element(By.ID, scf.expected_element_id)
        logging.info("expected element found")
    except (TimeoutException, NoSuchElementException) as e:
        logging.warning(f"failed to find expected element due to {type(e)}: {e}\n{traceback.format_exc()}")
        failures.append(f"failed to find expected element after login")


def check_site_single_attempt(os_selenium_handler: OSSeleniumHandler, scf: SiteCheckConfig) -> List[str]:
    """
    purpose: checks if a site is accessible
    :return:
    """
    driver = os_selenium_handler.get_chrome_driver()
    driver.implicitly_wait(20)

    failures = []
    for step in (
        lambda: goto_site(driver, scf, failures),
        lambda: enter_credentials_on_site(driver, scf, failures),
        lambda: find_expected_element(driver, scf, failures)
    ):
        step()
        if failures:
            if scf.screenshots:
                take_screenshot(driver)
            break
    driver.quit()
    return failures


def check_site(scf: SiteCheckConfig) -> List[str]:
    result = ["ERROR: no result obtained from checks"]
    os_selenium_handler = get_os_selenium_handler()
    for attempt in range(scf.max_check_attempts):
        logging.info(f"starting check_site attempt {attempt}")
        try:
            check_time_sec = int(scf.run_frequency_sec * 0.9 / scf.max_check_attempts)
            result = run_check(check_site_single_attempt, check_time_sec, os_selenium_handler, scf)
        except RunCheckTimeoutException:
            logging.warning(f"check_site attempt {attempt} timed out")
            result = ["check exceeded timeout"]

        if not result:
            logging.info(f"check_site attempt {attempt} passed")
            return result
        logging.warning(f"check_site attempt {attempt} failed")
        os_selenium_handler.kill_drivers()
        os_selenium_handler.delete_profile_data()

    logging.warning(f"all {scf.max_check_attempts} attempts for check_site exhausted, returning final result")
    return result
