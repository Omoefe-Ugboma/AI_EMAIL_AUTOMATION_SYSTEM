from email.mime.text import MIMEText
import base64


def send_reply(service, to, subject, body):
    message = MIMEText(body)

    message["to"] = to
    message["subject"] = f"Re: {subject}"

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()