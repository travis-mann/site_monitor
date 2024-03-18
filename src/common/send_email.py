import smtplib
import logging
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ENDPOINT = 'smtp.gmail.com'
PORT = 0


def send_mail_attempt_with_retries(server: smtplib.SMTP, msg: MIMEMultipart) -> None:
    max_attempts = 3
    retry_wait_seconds_multiplier = 3

    for attempt_idx in range(max_attempts):
        try:
            server.sendmail(msg.get('From'), msg["To"], msg.as_string())
            return
        except smtplib.SMTPDataError as e:
            logging.error(f"Failed to send email due to {type(e)}: {e}")
            sleep(attempt_idx * retry_wait_seconds_multiplier)
    raise RuntimeError(f'failed to send "{msg["Subject"]}" after {max_attempts} attempt(s)')


def send_email(
        subject: str,
        body: str,
        sender: str,
        recipients: list,
        sender_password: str,
        cc: list = None,
        endpoint: str = ENDPOINT,
        port: int = PORT
) -> None:
    """
    purpose: send an email
    :param subject:
    :param body:
    :param sender:
    :param recipients:
    :param cc:
    :return:
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    if isinstance(cc, list):
        msg["cc"] = ", ".join(cc)

    server = smtplib.SMTP(host=endpoint, port=port)
    server.starttls()
    server.login(sender, sender_password)
    send_mail_attempt_with_retries(server, msg)
