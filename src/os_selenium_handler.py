import os
import shutil
import logging
from typing import List
from pyvirtualdisplay import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service


PROFILE_DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "profile_data")


class OSSeleniumHandler:
    @staticmethod
    def is_this_os() -> bool:
        raise NotImplementedError()

    @staticmethod
    def kill_drivers() -> None:
        raise NotImplementedError()

    @staticmethod
    def get_chrome_driver() -> Chrome:
        raise NotImplementedError()

    @staticmethod
    def delete_profile_data() -> None:
        raise NotImplementedError()

    @staticmethod
    def get_chrome_driver_options() -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument(f"--user-data-dir={PROFILE_DATA_FOLDER}")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless=new')
        return options


class LinuxSeleniumHander(OSSeleniumHandler):
    @staticmethod
    def is_this_os() -> bool:
        return os.name == "posix"

    @staticmethod
    def kill_drivers():
        os.system("pkill chromedriver")
        os.system("pkill chrome")

    @staticmethod
    def get_chrome_driver():
        if not LinuxSeleniumHander._virtual_display_started():
            LinuxSeleniumHander._start_virtual_display()
        options = LinuxSeleniumHander.get_chrome_driver_options()
        return Chrome(
            options=options,
            service=Service(executable_path="/usr/lib/chromium-browser/chromedriver")
        )

    @staticmethod
    def delete_profile_data():
        logging.warning("deleting profile data")
        shutil.rmtree(PROFILE_DATA_FOLDER)
        logging.warning("profile data deleted")

    @staticmethod
    def _virtual_display_started() -> bool:
        return os.popen("ps").read().count('Xvfb') > 0

    @staticmethod
    def _start_virtual_display() -> None:
        logging.info("creating virtual display")
        display = Display(visible=0, size=(800, 600))
        display.start()
        logging.info("virtual display created")


class WindowsSeleniumHandler(OSSeleniumHandler):
    @staticmethod
    def is_this_os() -> bool:
        return os.name == "nt"

    @staticmethod
    def kill_drivers():
        os.system("taskkill /F /IM chromedriver.exe")
        os.system("taskkill /F /IM chrome.exe")

    @staticmethod
    def get_chrome_driver():
        return Chrome(options=WindowsSeleniumHandler.get_chrome_driver_options())

    @staticmethod
    def delete_profile_data():
        logging.warning("deleting profile data")
        shutil.rmtree(PROFILE_DATA_FOLDER)
        logging.warning("profile data deleted")


class OSHandlerNotFoundException(Exception):
    pass


def get_os_selenium_handler():
    handlers: List[OSSeleniumHandler] = [LinuxSeleniumHander, WindowsSeleniumHandler]
    for handler in handlers:
        if handler.is_this_os():
            return handler
    raise OSHandlerNotFoundException(f'no selenium handler found for "{os.name}"')
