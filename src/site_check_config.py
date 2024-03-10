import json


class SiteCheckConfig:
    def __init__(self, config_file_path: str):
        with open(config_file_path) as f:
            config = json.load(f)

        self.sender = config["sender"]
        self.site = config["site"]
        self.site_name = config["site_name"]
        self.username = config["username"]
        self.password = config["password"]
        self.username_id = config["username_id"]
        self.password_id = config["password_id"]
        self.expected_element_id = config["expected_element_id"]
        self.email_password = config["email_password"]
        self.alert_subject_prefix = config["alert_subject_prefix"]
        self.screenshots = config["screenshots"]
        self.run_frequency_sec = config["run_frequency_sec"]
        self.max_check_attempts = config["max_check_attempts"]
        self.receivers = [self.sender]
