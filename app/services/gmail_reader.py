import base64
import re

def fetch_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=10
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
            if payload["body"].get("data"):
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

def extract_name(sender):
    match = re.match(r"(.*)<", sender)
    if match:
        return match.group(1).strip()
    return "Customer"


def fetch_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=10
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

        name = extract_name(sender)

        body = ""

        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(
                        part["body"]["data"]
                    ).decode()
        else:
            if payload["body"].get("data"):
                body = base64.urlsafe_b64decode(
                    payload["body"]["data"]
                ).decode()

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "body": body,
            "sender": sender,
            "name": name
        })

    return emails

def get_or_create_label(service, label_name):
    """Get label ID by name, create if not exists."""
    labels = service.users().labels().list(userId='me').execute().get('labels', [])

    for label in labels:
        if label['name'] == label_name:
            return label['id']

    # Create label if not found
    label_object = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }

    created_label = service.users().labels().create(
        userId='me',
        body=label_object
    ).execute()

    return created_label['id']


def apply_label(service, msg_id, label_name):
    """Apply a label to an email."""
    label_id = get_or_create_label(service, label_name)

    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={
            "addLabelIds": [label_id]
        }
    ).execute()