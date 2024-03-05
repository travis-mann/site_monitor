import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ENDPOINT = 'smtp.gmail.com'
PORT = 0


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
    server.sendmail(msg.get('From'), msg["To"], msg.as_string())
