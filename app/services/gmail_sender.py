from email.mime.text import MIMEText
import base64


def send_reply(service, to, subject, body):
    message = MIMEText(body, "plain")

    message["to"] = to
    message["subject"] = f"Re: {subject}"

    # ✅ Important headers (reduce spam)
    message["Reply-To"] = "support@university.com"
    message["From"] = "AI Support Team <codejoe84@gmail.com>"

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()