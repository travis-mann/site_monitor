# --- imports ---
import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

from run_check import run_check
from check_site import check_site
from common.send_email import send_email
from common.exception_to_email import exception_to_email
from site_check_config import SiteCheckConfig


# --- glob ---
scf = SiteCheckConfig(os.path.join(PROJECT_DIR, "config.json"))


# --- func ---
@exception_to_email(f"{scf.site_name} Monitoring Tool", scf.sender, scf.receivers, scf.email_password)
def main():
    print("starting script")
    result = run_check(check_site, int(scf.run_frequency_sec * 0.95), scf)
    status = "FAIL" if result else "PASS"
    send_email(f"{scf.site_name} External Check {status}", ", ".join(result), scf.sender, scf.receivers, sender_password=scf.email_password)


if __name__ == '__main__':
    main()
