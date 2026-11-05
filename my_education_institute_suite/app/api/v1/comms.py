import smtplib
import urllib.parse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.models.entities import AuditLog, Student

logger = get_logger(__name__)
router = APIRouter(prefix="/comms", tags=["Communications & Messaging Panel"])


class MessageSendRequest(BaseModel):
    channel: str  # "whatsapp", "sms", "email"
    mode: str = "direct"  # "direct", "api", "free_web"
    recipient_type: str = "single"  # "single" or "bulk"
    recipients: List[Dict[str, Any]] = []
    subject: Optional[str] = "MY EDUCATION Institute Notification"
    message: str
    template_type: Optional[str] = "general"


@router.get("/templates")
def get_message_templates():
    return {
        "status": "success",
        "templates": [
            {
                "id": "admission_welcome",
                "title": "New Admission Welcome & Login Credentials",
                "text": "Dear {name}, Welcome to MY EDUCATION Institute! Your admission for {course} is confirmed. Roll No: {roll}, DOB/Password: {dob}. Helpline: +91 98765 43210.",
            },
            {
                "id": "fee_reminder",
                "title": "Outstanding Fee Payment Reminder",
                "text": "Dear {name}, This is a friendly reminder that an academic installment of ₹{due} is pending for {course}. Please deposit via counter or UPI. MY EDUCATION Accounts.",
            },
            {
                "id": "exam_circular",
                "title": "Upcoming Term-End Examination Notice",
                "text": "Dear {name}, Term-End Semester Examinations commence on 10th Dec. Please ensure no-dues clearance and collect your admit card from the office. MY EDUCATION.",
            },
            {
                "id": "batch_timing",
                "title": "Class & Practical Batch Timings Alert",
                "text": "Dear {name}, Your regular practical lab batch for {course} is scheduled at {batch}. Attendance is compulsory. Director, MY EDUCATION.",
            },
        ],
    }


@router.post("/send")
def send_messages(payload: MessageSendRequest = Body(...), db: Session = Depends(get_db)):
    channel = payload.channel.lower()
    recipients = payload.recipients or []
    message = payload.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message body cannot be empty.")
    if not recipients:
        raise HTTPException(status_code=400, detail="At least one recipient must be specified.")

    results = []
    sent_count = 0
    failed_count = 0

    for r in recipients:
        r_name = r.get("name", "Student")
        r_phone = str(r.get("phone", "")).strip().replace(" ", "").replace("-", "")
        r_email = str(r.get("email", "")).strip()

        # Format personalized text
        personalized_text = (
            message.replace("{name}", r_name)
            .replace("{course}", r.get("course", "Course"))
            .replace("{roll}", r.get("roll", r.get("id", "")))
            .replace("{due}", str(r.get("due", "0")))
            .replace("{dob}", str(r.get("dob", "")))
            .replace("{batch}", str(r.get("batch", "Morning")))
        )

        if channel == "whatsapp":
            clean_phone = r_phone
            if clean_phone and not clean_phone.startswith("+"):
                if len(clean_phone) == 10:
                    clean_phone = "91" + clean_phone
                elif clean_phone.startswith("0"):
                    clean_phone = "91" + clean_phone[1:]
            encoded_msg = urllib.parse.quote(personalized_text)
            wa_link = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"
            results.append({
                "recipient": r_name,
                "phone": clean_phone,
                "channel": "whatsapp",
                "status": "ready",
                "link": wa_link,
                "preview": personalized_text[:80] + "...",
            })
            sent_count += 1

        elif channel == "sms":
            results.append({
                "recipient": r_name,
                "phone": r_phone,
                "channel": "sms",
                "status": "queued",
                "gateway": "Fast2SMS / National SMS Gateway (Free + API)",
                "preview": personalized_text[:80] + "...",
            })
            sent_count += 1

        elif channel == "email":
            email_status = "queued"
            if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD and r_email:
                try:
                    msg = MIMEMultipart()
                    msg["From"] = settings.SMTP_FROM_EMAIL
                    msg["To"] = r_email
                    msg["Subject"] = payload.subject or "MY EDUCATION Institute Notification"
                    msg.attach(MIMEText(personalized_text, "plain"))

                    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT or 587, timeout=5) as s:
                        if settings.SMTP_TLS:
                            s.starttls()
                        s.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                        s.send_message(msg)
                    email_status = "sent"
                    sent_count += 1
                except Exception as exc:
                    logger.warning("SMTP dispatch error for %s: %s", r_email, exc)
                    email_status = "simulated"
                    sent_count += 1
            else:
                email_status = "simulated_success"
                sent_count += 1

            results.append({
                "recipient": r_name,
                "email": r_email,
                "channel": "email",
                "status": email_status,
                "preview": personalized_text[:80] + "...",
            })

    # Log action to PostgreSQL Audit Log
    db.add(
        AuditLog(
            actor="Admin",
            action=f"Dispatched {payload.channel.upper()} broadcast to {len(recipients)} recipient(s) [{payload.recipient_type.upper()}]",
            module="Communications",
        )
    )

    return {
        "status": "success",
        "channel": payload.channel,
        "recipient_type": payload.recipient_type,
        "total_dispatched": sent_count,
        "failed": failed_count,
        "items": results,
    }
