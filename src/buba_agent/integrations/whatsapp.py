# integrations/whatsapp.py

import os
import requests
from dotenv import load_dotenv
load_dotenv()


class WhatsAppIntegration:

    def __init__(self):

        self.token = os.getenv(
            "WHATSAPP_ACCESS_TOKEN"
        )

        self.phone_number_id = os.getenv(
            "WHATSAPP_PHONE_NUMBER_ID"
        )

        self.url = (
            f"https://graph.facebook.com/v25.0/"
            f"{self.phone_number_id}/messages"
        )

    def send_message(
        self,
        phone_number: str,
        message: str
    ):
        """
        Send a WhatsApp text message.
        """

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "messaging_product": "whatsapp",

            "to": phone_number,

            "type": "text",

            "text": {
                "body": message
            }
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=data
        )

        response.raise_for_status()

        result = response.json()

        return {
            "success": True,
            "message_id": result["messages"][0]["id"]
        }