import os
import sys
import logging
import time
from datetime import datetime


def get_project_folder() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_full_log_path(log_dir: str) -> str:
    log_file_name = datetime.now().strftime("%Y%m%d_runlog.txt")
    return os.path.join(log_dir, log_file_name)


def create_log_dir(log_path) -> None:
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def is_exceeding_retension_period(file_path: str, retension_period_days: int) -> bool:
    seconds_in_a_day = 86400
    oldest_allowable_modified_time = time.time() - seconds_in_a_day * retension_period_days
    file_modified_time = os.stat(file_path).st_mtime
    return file_modified_time < oldest_allowable_modified_time


def delete_logs_exceeding_retention_period(log_dir: str, retension_period_days: int) -> None:
    logging.info(f"checking for logs exceeding retention period of {retension_period_days} days")
    for log_file_name in os.listdir(log_dir):
        full_log_path = os.path.join(log_dir, log_file_name)
        if is_exceeding_retension_period(full_log_path, retension_period_days):
            logging.warning(f'deleting "{log_file_name}" because it exceeded the retention period of {retension_period_days} days.')
            os.remove(full_log_path)


def stream_root_logger_to_stdout():
    root_logger: logging.Logger = logging.getLogger()
    root_logger.addHandler(logging.StreamHandler(sys.stdout))


def apply_basic_config_to_root_logger(full_log_path: str):
    logging.basicConfig(
        format="[%(asctime)s %(levelname)s] %(msg)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        filename=full_log_path,
        filemode='a',
    )


def need_to_create_new_log(full_log_path) -> bool:
    return not os.path.exists(full_log_path)


def get_log_dir() -> str:
    return os.path.join(get_project_folder(), "log")


def configure_logging(retention_period_days: int) -> None:
    log_dir = get_log_dir()
    create_log_dir(log_dir)
    full_log_path = get_full_log_path(log_dir)
    delete_old_logs_after_logger_setup = need_to_create_new_log(full_log_path)
    apply_basic_config_to_root_logger(full_log_path)
    stream_root_logger_to_stdout()

    if delete_old_logs_after_logger_setup:
        delete_logs_exceeding_retention_period(log_dir, retention_period_days)
