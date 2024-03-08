import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)  # prevent module not found errors on scheduled tasks

# need to configure logging before importing other modules which use it
from common.setup_logging import init_root_logger, logging
init_root_logger()

from run_check import run_check
from check_site import check_site
from common.send_email import send_email
from site_check_config import SiteCheckConfig
from common.exception_to_email import exception_to_email

scf = SiteCheckConfig(os.path.join(PROJECT_DIR, "config.json"))


@exception_to_email(f"{scf.site_name} Monitoring Tool", scf.sender, scf.receivers, scf.email_password)
def main():
    logging.info("starting script")
    result = run_check(check_site, int(scf.run_frequency_sec * 0.95), scf)
    status = "FAIL" if result else "PASS"
    send_email(f"{scf.site_name} External Check {status}", ", ".join(result), scf.sender, scf.receivers, sender_password=scf.email_password)
    logging.info("done")


if __name__ == '__main__':
    main()
