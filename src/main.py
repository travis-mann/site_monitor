import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)  # prevent module not found errors on scheduled tasks

# need to configure logging before importing other modules which use it
from common.setup_logging import init_root_logger, logging
init_root_logger()

from run_check import run_check
from check_site import check_site
from result_handler import ResultHandler
from site_check_config import SiteCheckConfig
from common.exception_to_email import exception_to_email

SCF = SiteCheckConfig(os.path.join(PROJECT_DIR, "config.json"))


@exception_to_email(f"{SCF.site_name} Monitoring Tool", SCF.sender, SCF.receivers, SCF.email_password)
def main():
    logging.info("starting script")
    result = run_check(check_site, int(SCF.run_frequency_sec * 0.95), SCF)
    logging.info(f"check results: {result}")
    ResultHandler.notify_user_with_result(result, SCF)
    ResultHandler.store_result(result)
    logging.info("done")


if __name__ == '__main__':
    main()
