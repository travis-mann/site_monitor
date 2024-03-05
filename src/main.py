# --- imports ---
import os
from selenium.webdriver.common.by import By

from run_check import run_check
from check_site import check_site
from common.send_email import send_email
from common.exception_to_email import exception_to_email


# --- glob ---
SENDER = os.environ["SENDER"]
SITE = os.environ["SITE"]
SITE_NAME = os.environ["SITE_NAME"]
USERNAME_ID = os.environ["USERNAME_ID"]
PASSWORD_ID = os.environ["PASSWORD_ID"]
EXPECTED_ELEMENT_ID = os.environ["PASSWORD_ID"]
SENDER_EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
RECEIVERS = [SENDER]


# --- func ---
@exception_to_email(f"{SITE_NAME} Monitoring Tool", SENDER, RECEIVERS, SENDER_EMAIL_PASSWORD)
def main():
    print("starting script")
    result = run_check(check_site, 9*60, SITE, (By.ID, USERNAME_ID), (By.ID, PASSWORD_ID), (By.ID, EXPECTED_ELEMENT_ID))
    status = "FAIL" if result else "PASS"
    send_email(f"{SITE_NAME} External Check {status}", ", ".join(result), SENDER, RECEIVERS, sender_password=SENDER_EMAIL_PASSWORD)


if __name__ == '__main__':
    main()
