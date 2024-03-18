import json
import os.path
from typing import Dict
from datetime import datetime, time, timedelta

LOGS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")


def get_remaining_runs_today(run_frequency_sec: int) -> int:
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    seconds_left_today = (datetime.combine(tomorrow, time.min) - now).total_seconds()
    return int(seconds_left_today // run_frequency_sec)


def get_total_expected_runs(run_frequency_sec: int) -> int:
    total_log_count = len(os.listdir(LOGS_FOLDER))
    total_runs = total_log_count * int(86400 / run_frequency_sec)
    total_expected_runs = total_runs - get_remaining_runs_today(run_frequency_sec)
    return total_expected_runs


def extract_log_lines(criteria_action_map: Dict[callable, callable]) -> None:
    for log in os.listdir(LOGS_FOLDER):
        full_log_path = os.path.join(LOGS_FOLDER, log)
        with open(full_log_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            data = json.loads(line)

            for criteria_func, action_func in criteria_action_map.items():
                if criteria_func(data):
                    action_func(data)


if __name__ == "__main__":
    pass_count = 0
    fail_count = 0
    errors = []

    def is_error(data: dict) -> bool:
        return data["level"] == "ERROR"

    def is_pass(data: dict) -> bool:
        return data["message"] == "site is currently accessible"

    def is_fail(data: dict) -> bool:
        return data["message"] == "site is currently inaccessible"

    def store_error(data: dict) -> None:
        errors.append(data)

    def increment_pass_count(_: dict) -> None:
        global pass_count
        pass_count += 1

    def increment_fail_count(_: dict) -> None:
        global fail_count
        fail_count += 1

    criteria_action_map = {
        is_error: store_error,
        is_pass: increment_pass_count,
        is_fail: increment_fail_count
    }
    total_expected_runs = get_total_expected_runs(600)
    extract_log_lines(criteria_action_map)
    print(f"{pass_count}/{total_expected_runs} check(s) passed")
    print(f"{fail_count}/{total_expected_runs} check(s) failed")
    print(f"{total_expected_runs - pass_count - fail_count} check(s) missed")
    print(f"ERRORS:")
    for error in errors:
        print(error)
