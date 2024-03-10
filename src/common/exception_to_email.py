import logging
import traceback
from src.common.send_email import send_email


def exception_to_email(name: str, sender: str, receivers: list, sender_password: str) -> callable:
    """
    purpose: function wrapper to convert any uncaught exceptions into an email notification
    """
    def decorator(func: callable):
        def wrapper():
            try:
                return func()
            except Exception as e:
                logging.error(f"failed to run {name} due to {type(e)}: {e}\n{traceback.format_exc()}")
                subject = f"Failed to run {name}"
                send_email(subject, "", sender, receivers, sender_password)
                logging.info(f'email notification sent with subject "{subject}"')
        return wrapper

    return decorator
