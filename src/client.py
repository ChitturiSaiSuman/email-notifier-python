from datetime import datetime


class Client:
    def __init__(self, service):
        self.service = service

    def get_unread_emails(self, last_checked: datetime):
        last_checked_timestamp = int(last_checked.timestamp())
        query = f"is:unread after:{last_checked_timestamp}"

        results = self.service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])

        unread_emails = []

        for msg in messages:
            msg_details = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["From", "Subject"],
                )
                .execute()
            )

            headers = msg_details["payload"]["headers"]

            email_info = {
                "id": msg["id"],
                "from": next(
                    header["value"] for header in headers if header["name"] == "From"
                ),
                "subject": next(
                    header["value"] for header in headers if header["name"] == "Subject"
                ),
                "link": f"https://mail.google.com/mail/u/0/#inbox/{msg['id']}",
            }

            unread_emails.append(email_info)

        return unread_emails
