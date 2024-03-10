import pickle
from typing import List
from common.send_email import send_email
from site_check_config import SiteCheckConfig
import logging


class ResultHandler:
    result_pickle_file_path = "result.pk"
    pass_str = "PASS"
    fail_str = "FAIL"
    issues_resolved_str = "Issues Resolved"

    @staticmethod
    def notify_user_with_result(check_failure_strs: List[str], scf: SiteCheckConfig) -> None:
        is_site_accessible = ResultHandler._is_site_accessible(check_failure_strs)
        logging.info(f"site is currently {'accessible' if is_site_accessible else 'inaccessible'}")
        if is_new_success := ResultHandler._is_new_success(is_site_accessible):
            logging.info(f"{scf.site_name} is available again after a previously detected outage")
        if is_new_failure := ResultHandler._is_new_failure(is_site_accessible):
            logging.warning(f"new {scf.site_name} outage detected")
        subject = ResultHandler._get_subject(is_site_accessible, is_new_success, is_new_failure, scf)
        body = ", ".join(check_failure_strs)
        send_email(subject, body, scf.sender, scf.receivers, sender_password=scf.email_password)
        logging.info(f'email notification sent with subject "{subject}"')

    @staticmethod
    def store_result(check_failure_strs: List[str]) -> None:
        result = ResultHandler._is_site_accessible(check_failure_strs)
        with open(ResultHandler.result_pickle_file_path, 'wb') as f:
            pickle.dump(result, f)

    @staticmethod
    def _is_site_accessible(check_failure_strs: List[str]) -> bool:
        return not bool(check_failure_strs)

    @staticmethod
    def _get_status_str(is_site_accessible: bool, is_new_success: bool) -> str:
        if is_new_success:
            return ResultHandler.issues_resolved_str
        elif is_site_accessible:
            return ResultHandler.pass_str
        else:
            return ResultHandler.fail_str

    @staticmethod
    def _is_new_failure(is_site_accessible: bool) -> bool:
        site_previously_accessible = ResultHandler._get_previous_result()
        is_new_failure = not is_site_accessible and not site_previously_accessible is False
        return is_new_failure

    @staticmethod
    def _is_new_success(is_site_accessible: bool) -> bool:
        if not is_site_accessible:
            return False
        site_previously_accessible = ResultHandler._get_previous_result()
        is_new_success = is_site_accessible and site_previously_accessible is False
        return is_new_success

    @staticmethod
    def _get_previous_result() -> bool | None:
        try:
            return ResultHandler._get_pickled_result()
        except FileNotFoundError:
            return None

    @staticmethod
    def _get_pickled_result() -> bool:
        with open(ResultHandler.result_pickle_file_path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def _get_subject_prefix(is_new_failure: bool, alert_subject_prefix: str) -> str:
        return alert_subject_prefix + " " if is_new_failure else ""

    @staticmethod
    def _get_subject(is_site_accessible: bool, is_new_success: bool, is_new_failure: bool, scf: SiteCheckConfig):
        return f"{ResultHandler._get_subject_prefix(is_new_failure, scf.alert_subject_prefix)}{scf.site_name} Check {ResultHandler._get_status_str(is_site_accessible, is_new_success)}"
