import requests

def send_email_notification(event, email, username):
    payload = {
        "event": event,
        "email": email,
        "username": username
    }

    try:
        requests.post("http://localhost:3000/dev/send-email", json=payload, timeout=5)
    except Exception as e:
        print("Email service down:", e)

