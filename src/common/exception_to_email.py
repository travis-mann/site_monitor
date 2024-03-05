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
                print(f"failed to run {name} due to {type(e)}: {e}")
                send_email(f"Failed to run {name}", "", sender, receivers, sender_password)
        return wrapper

    return decorator
