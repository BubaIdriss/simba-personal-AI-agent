# integrations/google.py

import os
import base64

from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


# Permissions our application requests from Google
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/contacts.readonly",
]

class GoogleIntegration:

    def __init__(self):
        """
        Load the user's Google OAuth credentials.

        token.json should contain the user's OAuth token.
        """

        self.creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

        #flow = InstalledAppFlow.from_client_secrets_file(
        #    "credentials.json",
        #    SCOPES
        #)

        #creds = flow.run_local_server(port=0)
#
        #with open("token.json", "w") as token:
        #    token.write(creds.to_json())

        self.gmail = build(
            "gmail",
            "v1",
            credentials=self.creds
        )

        self.calendar = build(
            "calendar",
            "v3",
            credentials=self.creds
        )

        self.people = build(
            "people",
            "v1",
            credentials=self.creds
        )

    # ------------------------------------------------
    # GMAIL
    # ------------------------------------------------

    def send_email(
        self,
        to: str,
        subject: str,
        body: str
    ):
        """
        Send an email through the user's Gmail account.
        """

        message = MIMEText(body)

        message["to"] = to
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        result = self.gmail.users().messages().send(
            userId="me",
            body={
                "raw": raw_message
            }
        ).execute()

        return {
            "success": True,
            "message_id": result["id"],
            "to": to,
            "subject": subject
        }

    # ------------------------------------------------
    # READ EMAILS
    # ------------------------------------------------

    def search_emails(
        self,
        query: str,
        max_results: int = 10
    ):
        """
        Search the user's Gmail.

        Examples:

        from:john@gmail.com
        subject:meeting
        newer_than:7d
        """

        result = self.gmail.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results
        ).execute()

        messages = result.get("messages", [])

        emails = []

        for message in messages:

            email = self.gmail.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "To",
                    "Subject",
                    "Date"
                ]
            ).execute()

            headers = email["payload"].get(
                "headers",
                []
            )

            data = {}

            for header in headers:
                data[header["name"]] = header["value"]

            emails.append(data)

        return emails

    # ------------------------------------------------
    # GOOGLE CONTACTS
    # ------------------------------------------------

    def get_contacts(
        self,
        max_results: int = 100
    ):
        """
        Get contacts and their email addresses
        from the user's Google Contacts.
        """

        result = self.people.people().connections().list(
            resourceName="people/me",
            pageSize=max_results,
            personFields="names,emailAddresses,phoneNumbers"
        ).execute()

        contacts = []

        for person in result.get("connections", []):

            names = person.get("names", [])

            name = (
                names[0].get("displayName")
                if names
                else None
            )

            emails = person.get(
                "emailAddresses",
                []
            )

            email_addresses = [
                email.get("value")
                for email in emails
            ]

            contacts.append({
                "name": name,
                "emails": email_addresses
            })

        return contacts

    # ------------------------------------------------
    # FIND CONTACT
    # ------------------------------------------------

    def find_contact(
        self,
        name: str
    ):
        """
        Find a person's email address
        from Google Contacts.
        """

        contacts = self.get_contacts()

        name_lower = name.lower()

        matches = []

        for contact in contacts:

            contact_name = contact.get("name")

            if contact_name and name_lower in contact_name.lower():

                matches.append(contact)

        return matches

    # ------------------------------------------------
    # CALENDAR
    # ------------------------------------------------

    def get_calendar_events(
        self,
        max_results: int = 10
    ):
        """
        Read upcoming calendar events.
        """

        result = self.calendar.events().list(
            calendarId="primary",
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
            timeMin=datetime.utcnow().isoformat() + "Z"
        ).execute()

        events = []

        for event in result.get("items", []):

            events.append({
                "id": event.get("id"),
                "title": event.get("summary"),
                "start": event.get("start"),
                "end": event.get("end"),
                "description": event.get("description"),
                "location": event.get("location")
            })

        return events

    # ------------------------------------------------
    # CREATE CALENDAR EVENT
    # ------------------------------------------------

    def create_event(
        self,
        title: str,
        start: str,
        end: str,
        description: str = "",
        location: str = ""
    ):
        """
        Create an event in the user's primary calendar.

        start/end example:

        2026-09-25T14:00:00+01:00
        """

        event = {
            "summary": title,
            "description": description,
            "location": location,

            "start": {
                "dateTime": start,
                "timeZone": "Africa/Lagos"
            },

            "end": {
                "dateTime": end,
                "timeZone": "Africa/Lagos"
            }
        }

        result = self.calendar.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        return {
            "success": True,
            "event_id": result["id"],
            "title": result["summary"],
            "start": result["start"],
            "end": result["end"],
            "link": result.get("htmlLink")
        }