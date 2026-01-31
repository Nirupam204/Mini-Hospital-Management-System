import json
import smtplib
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_gmail@gmail.com"
SMTP_PASS = "your_app_password"


def send_email_smtp(to_email, subject, body):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


def send_email(event, context):
    data = json.loads(event.get("body") or "{}")

    email_type = data.get("type")
    to_email = data.get("to_email")
    name = data.get("name", "")

    if not email_type or not to_email:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "type and to_email are required"}),
        }

    if email_type == "SIGNUP_WELCOME":
        subject = "Welcome to Mini HMS"
        body = f"Hello {name},\n\nWelcome to Mini Hospital Management System.\n"
    elif email_type == "BOOKING_CONFIRMATION":
        subject = "Appointment Confirmed"
        body = f"Hello {name},\n\nYour appointment booking is confirmed.\n"
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "invalid email type"}),
        }

    send_email_smtp(to_email, subject, body)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "email sent successfully"}),
    }
