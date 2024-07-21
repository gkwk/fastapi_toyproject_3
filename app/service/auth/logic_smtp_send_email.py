import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config.config import get_settings


def logic_smtp_send_email(email_to: str, email_subject: str, email_body: str):
    email_account = get_settings().SMTP_ACCOUNT
    email_account_password = get_settings().SMTP_PASSWORD

    message = MIMEMultipart()
    message["From"] = email_account
    message["To"] = email_to
    message["Subject"] = email_subject

    message.attach(MIMEText(email_body, "html"))

    with smtplib.SMTP(get_settings().SMTP_DOMAIN, get_settings().SMTP_PORT) as server:
        server.starttls()
        server.login(email_account, email_account_password)
        server.send_message(message)
