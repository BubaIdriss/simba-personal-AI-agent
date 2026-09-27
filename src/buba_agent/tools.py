# tools.py

from langchain.tools import tool
from langgraph.types import interrupt
from datetime import datetime
from zoneinfo import ZoneInfo

from .integrations.google import GoogleIntegration
from .integrations.whatsapp import WhatsAppIntegration
from .integrations.web_search import WebSearch


# --------------------------------------------------
# Create our integration objects
# --------------------------------------------------

google = GoogleIntegration()
whatsapp = WhatsAppIntegration()
web = WebSearch()


# ==================================================
# EMAIL
# ==================================================

@tool
def send_email(
    to: str,
    subject: str,
    body: str
):
    """
    Send an email through the user's Gmail account.

    This action requires human approval before the
    email is actually sent.
    """

    # --------------------------------------------------
    # STOP THE AGENT AND ASK THE HUMAN
    #
    # Everything inside this dictionary will be sent
    # back to the application so we can display it.
    # --------------------------------------------------

    approval = interrupt({
        "action": "send_email",

        "message": "The agent wants to send this email.",

        "to": to,

        "subject": subject,

        "body": body,
    })

    # --------------------------------------------------
    # The human rejected the action
    # --------------------------------------------------

    if approval != "approve":
        return (
            "The user rejected the email. "
            "Do not send it."
        )

    # --------------------------------------------------
    # ONLY NOW do we actually send the email
    # --------------------------------------------------

    result = google.send_email(
        to=to,
        subject=subject,
        body=body
    )

    return result


# Time abd Date
@tool
def get_current_datetime():
    """
    Get the current date and time in Nigeria.

    Use this whenever the user asks for the current time,
    current date, today, tomorrow, etc.
    """

    nigeria_time = datetime.now(
        ZoneInfo("Africa/Lagos")
    )

    return {
        "date": nigeria_time.strftime("%Y-%m-%d"),
        "time": nigeria_time.strftime("%H:%M:%S"),
        "day": nigeria_time.strftime("%A"),
        "timezone": "Africa/Lagos",
        "datetime": nigeria_time.isoformat()
    }


# CALENDAR
@tool
def schedule_event(
    title: str,
    start: str,
    end: str,
    description: str = "",
    location: str = ""
):
    """
    Create a Google Calendar event.

    Human approval is required before creating it.
    """

    approval = interrupt({
        "action": "schedule_event",

        "message": (
            "The agent wants to create "
            "this calendar event."
        ),

        "title": title,

        "start": start,

        "end": end,

        "description": description,

        "location": location,
    })

    # Human rejected

    if approval != "approve":
        return (
            "The user rejected the calendar event. "
            "Do not create it."
        )

    # Create the event only after approval

    result = google.create_event(
        title=title,
        start=start,
        end=end,
        description=description,
        location=location
    )

    return result


# SEARCH EMAILS
@tool
def search_emails(query: str):
    """
    Search the user's Gmail.
    """

    return google.search_emails(query)


# CONTACTS
@tool
def find_contact(name: str):
    """
    Find a contact from Google Contacts.
    """

    return google.find_contact(name)


@tool
def get_contacts():
    """
    Get contacts and their email addresses.
    """

    return google.get_contacts()


# CALENDAR
@tool
def get_calendar_events():
    """
    Read upcoming Google Calendar events.
    """

    return google.get_calendar_events()


# WEB SEARCH
@tool
def search_web(query: str):
    """
    Search the internet using Tavily.
    """

    return web.search(query)