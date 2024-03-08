import os.path
import sys
import unittest
from typing import List
from unittest.mock import patch

project_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(project_dir, "src"))

from src.result_handler import ResultHandler
from src.site_check_config import SiteCheckConfig


class MockSiteCheckConfig(SiteCheckConfig):
    site_name = "test_name"
    alert_subject_prefix = "[Test Alert]"


class TestResultHandler(unittest.TestCase):

    @patch('src.site_check_config.SiteCheckConfig')
    def setUp(self, MockSiteCheckConfig):
        self.mock_scf = MockSiteCheckConfig()
        self.mock_scf.site_name = "Test Site"
        self.mock_scf.alert_subject_prefix = "[Test Alert]"

    def get_subject_from_result_scenario(self, previous_result: List[str], current_result: List[str]) -> str:
        ResultHandler.store_result(previous_result)
        is_site_accessible = ResultHandler._is_site_accessible(current_result)
        is_new_success = ResultHandler._is_new_success(is_site_accessible)
        is_new_failure = ResultHandler._is_new_failure(is_site_accessible)
        return ResultHandler._get_subject(is_site_accessible, is_new_success, is_new_failure, self.mock_scf)

    def test_pass_subject(self):
        subject = self.get_subject_from_result_scenario([], [])
        expected_str_in_subject = ResultHandler.pass_str
        self.assertEqual(len(expected_str_in_subject) > 0, True)
        self.assertIn(expected_str_in_subject, subject)

    def test_fail_subject(self):
        subject = self.get_subject_from_result_scenario(["test_failure"], ["test_failure"])
        expected_str_in_subject = ResultHandler.fail_str
        self.assertEqual(len(expected_str_in_subject) > 0, True)
        self.assertIn(expected_str_in_subject, subject)

    def test_alert_subject(self):
        subject = self.get_subject_from_result_scenario([], ["test_failure"])
        expected_str_in_subject = self.mock_scf.alert_subject_prefix
        for expected_str_in_subject in [self.mock_scf.alert_subject_prefix, ResultHandler.fail_str]:
            self.assertEqual(len(expected_str_in_subject) > 0, True)
            self.assertIn(expected_str_in_subject, subject)

    def test_issues_resolved_subject(self):
        subject = self.get_subject_from_result_scenario(["test_failure"], [])
        expected_str_in_subject = ResultHandler.issues_resolved_str
        self.assertEqual(len(expected_str_in_subject) > 0, True)
        self.assertIn(expected_str_in_subject, subject)
