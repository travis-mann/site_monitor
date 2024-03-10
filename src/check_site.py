from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from typing import List
import logging

from os_selenium_handler import OSSeleniumHandler, get_os_selenium_handler
from run_check import run_check, RunCheckTimeoutException
from site_check_config import SiteCheckConfig


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
            os_selenium_handler.kill_drivers()
            result = ["check exceeded timeout"]
        if not result:
            logging.info(f"check_site attempt {attempt} passed")
            return result
        logging.warning(f"check_site attempt {attempt} failed")
    logging.warning(f"all {scf.max_check_attempts} attempts for check_site exhausted, returning final result")
    return result


def check_site_single_attempt(os_selenium_handler: OSSeleniumHandler, scf: SiteCheckConfig) -> List[str]:
    """
    purpose: checks if a site is accessible
    :return:
    """
    driver = os_selenium_handler.get_chrome_driver()
    driver.implicitly_wait(20)

    logging.info(f"going to {scf.site}")
    driver.get(scf.site)

    logging.info("entering credentials")
    driver.find_element(By.ID, scf.username_id).send_keys(scf.username)
    driver.find_element(By.ID, scf.password_id).send_keys(scf.password + Keys.ENTER)

    logging.info("checking for expected element")
    try:
        driver.find_element(By.ID, scf.expected_element_id)
        logging.info("expected element found")
        driver.quit()
        return []
    except TimeoutException:
        driver.quit()
        return [f"failed to reach {scf.site_name} after login"]
