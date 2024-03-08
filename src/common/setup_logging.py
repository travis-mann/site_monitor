import os
import logging
from datetime import datetime


def get_project_folder() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_full_log_path() -> str:
    project_folder = get_project_folder()
    partial_log_path = datetime.now().strftime("log\%Y\%m\%Y%m%d_site_monitor_log.txt")
    return os.path.join(project_folder, partial_log_path)


def create_log_path(log_path) -> None:
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_path):
        os.makedirs(log_dir)


def configure_logging() -> None:
    full_log_path = get_full_log_path()
    create_log_path(full_log_path)
    logging.basicConfig(
        format="[%(asctime)s %(levelname)s] %(msg)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        filename=full_log_path,
        filemode='a',
    )
