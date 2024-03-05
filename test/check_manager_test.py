import unittest
from src.run_check import run_check, RunCheckTimeoutException
from time import sleep


def simple_func():
    return []


def long_func():
    sleep(10)


class TestRunCheck(unittest.TestCase):

    def test_happy_path(self):
        self.assertEqual(run_check(simple_func, 10), [])

    def test_timeout(self):
        with self.assertRaises(RunCheckTimeoutException):
            run_check(long_func, 1)
