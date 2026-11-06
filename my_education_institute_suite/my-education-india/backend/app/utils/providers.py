import smtplib
from email.message import EmailMessage
from typing import Any, Dict, Protocol
import httpx
from app.core.config import get_settings
from app.logs.logger import app_logger


class EmailProviderProtocol(Protocol):
    async def send_email(self, recipient: str, subject: str, html_body: str) -> Dict[str, Any]: ...


class SMSProviderProtocol(Protocol):
    async def send_sms(self, phone_number: str, message: str, template_id: str | None = None) -> Dict[str, Any]: ...


class WhatsAppProviderProtocol(Protocol):
    async def send_whatsapp(self, phone_number: str, template_name: str, parameters: list[str]) -> Dict[str, Any]: ...


class ConfigurableSMTPProvider:
    def __init__(self, host: str, port: int, username: str, password: str, from_email: str, use_tls: bool = True) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.use_tls = use_tls

    async def send_email(self, recipient: str, subject: str, html_body: str) -> Dict[str, Any]:
        if not self.host:
            raise ValueError("SMTP host is not configured.")
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.from_email
        msg["To"] = recipient
        msg.set_content("Please view this message in an HTML-compatible email client.")
        msg.add_alternative(html_body, subtype="html")

        with smtplib.SMTP(self.host, self.port, timeout=15) as server:
            if self.use_tls:
                server.starttls()
            if self.username and self.password:
                server.login(self.username, self.password)
            server.send_message(msg)
        app_logger.info(f"Dispatched transactional email to {recipient}")
        return {"status": "sent", "recipient": recipient}


class ConfigurableSMSProvider:
    def __init__(self, endpoint_url: str, api_key: str, sender_id: str) -> None:
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.sender_id = sender_id

    async def send_sms(self, phone_number: str, message: str, template_id: str | None = None) -> Dict[str, Any]:
        if not self.endpoint_url or not self.api_key:
            raise ValueError("SMS gateway endpoint and API key must be configured.")
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                self.endpoint_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "sender": self.sender_id,
                    "mobile": phone_number,
                    "message": message,
                    "template_id": template_id,
                },
            )
            response.raise_for_status()
            return response.json()


class ConfigurableWhatsAppProvider:
    def __init__(self, phone_number_id: str, access_token: str) -> None:
        self.phone_number_id = phone_number_id
        self.access_token = access_token

    async def send_whatsapp(self, phone_number: str, template_name: str, parameters: list[str]) -> Dict[str, Any]:
        if not self.phone_number_id or not self.access_token:
            raise ValueError("WhatsApp Cloud API credentials are not configured.")
        url = f"https://graph.facebook.com/v20.0/{self.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "en"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [{"type": "text", "text": p} for p in parameters],
                    }
                ],
            },
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()
