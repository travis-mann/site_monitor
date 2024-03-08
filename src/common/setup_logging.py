import os
import json
import atexit
import logging
import logging.config
import logging.handlers


def get_project_folder() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_log_dir(config: dict) -> None:
    partial_log_path = "/".join(config["handlers"]["file"]["filename"].split("/")[:-1])
    complete_log_dir = os.path.join(get_project_folder(), partial_log_path)
    if not os.path.exists(complete_log_dir):
        os.makedirs(complete_log_dir)


def init_root_logger() -> None:
    with open("logging_config.json", 'r') as f:
        config = json.load(f)
    create_log_dir(config)
    logging.config.dictConfig(config)
