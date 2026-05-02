import base64

def fetch_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        payload = data["payload"]
        headers = payload["headers"]

        subject = ""
        sender = ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            if h["name"] == "From":
                sender = h["value"]

        body = ""

        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(
                        part["body"]["data"]
                    ).decode()
        else:
            body = base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode()

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "body": body,
            "sender": sender
        })

    return emails