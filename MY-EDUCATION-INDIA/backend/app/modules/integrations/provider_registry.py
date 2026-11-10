"""
Universal Provider Registry
Maintains catalog of plug-and-play provider templates across:
SMS, WhatsApp, Email, Push, Payment, Video, Storage, AI, Maps, and OTP.
"""
from typing import List, Dict, Any, Optional

TEMPLATES = [
    # SMS
    {"provider_key": "fast2sms", "display_name": "Fast2SMS India", "category": "SMS", "auth_type": "CUSTOM_HEADER", "suggested_base_url": "https://www.fast2sms.com/dev/bulkV2", "required_credential_fields": ["header_authorization"], "doc_url": "https://docs.fast2sms.com"},
    {"provider_key": "msg91", "display_name": "MSG91 Communications", "category": "SMS", "auth_type": "CUSTOM_HEADER", "suggested_base_url": "https://api.msg91.com/api/v5", "required_credential_fields": ["header_authkey"], "doc_url": "https://docs.msg91.com"},
    {"provider_key": "twilio_sms", "display_name": "Twilio Programmable SMS", "category": "SMS", "auth_type": "BASIC", "suggested_base_url": "https://api.twilio.com/2010-04-01", "required_credential_fields": ["username", "password"], "doc_url": "https://www.twilio.com/docs/sms"},
    {"provider_key": "aws_sns", "display_name": "Amazon SNS SMS", "category": "SMS", "auth_type": "API_KEY", "suggested_base_url": "https://sns.ap-south-1.amazonaws.com", "required_credential_fields": ["api_key", "secret"], "doc_url": "https://docs.aws.amazon.com/sns"},

    # WhatsApp
    {"provider_key": "meta_whatsapp", "display_name": "Meta WhatsApp Cloud API", "category": "WHATSAPP", "auth_type": "BEARER", "suggested_base_url": "https://graph.facebook.com/v19.0", "required_credential_fields": ["token", "phone_number_id"], "doc_url": "https://developers.facebook.com/docs/whatsapp"},
    {"provider_key": "interakt", "display_name": "Interakt WhatsApp Platform", "category": "WHATSAPP", "auth_type": "BASIC", "suggested_base_url": "https://api.interakt.ai/v1", "required_credential_fields": ["username", "password"], "doc_url": "https://docs.interakt.shop"},
    {"provider_key": "gupshup_wa", "display_name": "Gupshup Enterprise WhatsApp", "category": "WHATSAPP", "auth_type": "CUSTOM_HEADER", "suggested_base_url": "https://api.gupshup.io/sm/api/v1", "required_credential_fields": ["header_apikey"], "doc_url": "https://docs.gupshup.io"},

    # Email
    {"provider_key": "sendgrid", "display_name": "Twilio SendGrid Email", "category": "EMAIL", "auth_type": "BEARER", "suggested_base_url": "https://api.sendgrid.com/v3", "required_credential_fields": ["token"], "doc_url": "https://docs.sendgrid.com"},
    {"provider_key": "amazon_ses", "display_name": "Amazon Simple Email Service (SES)", "category": "EMAIL", "auth_type": "API_KEY", "suggested_base_url": "https://email.ap-south-1.amazonaws.com", "required_credential_fields": ["api_key", "secret"], "doc_url": "https://docs.aws.amazon.com/ses"},
    {"provider_key": "smtp_custom", "display_name": "Custom SMTP Server", "category": "EMAIL", "auth_type": "BASIC", "suggested_base_url": "smtp://smtp.office365.com:587", "required_credential_fields": ["username", "password", "port"], "doc_url": "https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol"},

    # Push
    {"provider_key": "firebase_fcm", "display_name": "Firebase Cloud Messaging (FCM)", "category": "PUSH", "auth_type": "BEARER", "suggested_base_url": "https://fcm.googleapis.com/v1", "required_credential_fields": ["token", "project_id"], "doc_url": "https://firebase.google.com/docs/cloud-messaging"},
    {"provider_key": "onesignal", "display_name": "OneSignal Push Notifications", "category": "PUSH", "auth_type": "CUSTOM_HEADER", "suggested_base_url": "https://onesignal.com/api/v1", "required_credential_fields": ["header_Authorization", "app_id"], "doc_url": "https://documentation.onesignal.com"},

    # Payment
    {"provider_key": "razorpay", "display_name": "Razorpay Payments India", "category": "PAYMENT", "auth_type": "BASIC", "suggested_base_url": "https://api.razorpay.com/v1", "required_credential_fields": ["username", "password"], "doc_url": "https://razorpay.com/docs/api"},
    {"provider_key": "cashfree", "display_name": "Cashfree Payments", "category": "PAYMENT", "auth_type": "CUSTOM_HEADER", "suggested_base_url": "https://api.cashfree.com/pg", "required_credential_fields": ["header_x-client-id", "header_x-client-secret"], "doc_url": "https://docs.cashfree.com"},
    {"provider_key": "stripe", "display_name": "Stripe Global Payments", "category": "PAYMENT", "auth_type": "BEARER", "suggested_base_url": "https://api.stripe.com/v1", "required_credential_fields": ["token"], "doc_url": "https://stripe.com/docs/api"},

    # Video
    {"provider_key": "zoom_video", "display_name": "Zoom Video Communications", "category": "VIDEO", "auth_type": "OAUTH2", "suggested_base_url": "https://api.zoom.us/v2", "required_credential_fields": ["client_id", "client_secret", "account_id"], "doc_url": "https://marketplace.zoom.us/docs"},
    {"provider_key": "google_meet", "display_name": "Google Meet Enterprise", "category": "VIDEO", "auth_type": "OAUTH2", "suggested_base_url": "https://meet.googleapis.com/v2", "required_credential_fields": ["client_id", "client_secret"], "doc_url": "https://developers.google.com/meet"},

    # Storage
    {"provider_key": "aws_s3", "display_name": "Amazon S3 Object Storage", "category": "STORAGE", "auth_type": "API_KEY", "suggested_base_url": "https://s3.ap-south-1.amazonaws.com", "required_credential_fields": ["api_key", "secret", "bucket"], "doc_url": "https://docs.aws.amazon.com/s3"},
    {"provider_key": "cloudflare_r2", "display_name": "Cloudflare R2 Storage", "category": "STORAGE", "auth_type": "API_KEY", "suggested_base_url": "https://r2.cloudflarestorage.com", "required_credential_fields": ["api_key", "secret", "bucket"], "doc_url": "https://developers.cloudflare.com/r2"},

    # AI
    {"provider_key": "openai", "display_name": "OpenAI (GPT-4o & Embeddings)", "category": "AI", "auth_type": "BEARER", "suggested_base_url": "https://api.openai.com/v1", "required_credential_fields": ["token"], "doc_url": "https://platform.openai.com/docs"},
    {"provider_key": "google_gemini", "display_name": "Google Gemini Generative AI", "category": "AI", "auth_type": "CUSTOM_HEADER", "suggested_base_url": "https://generativelanguage.googleapis.com/v1beta", "required_credential_fields": ["header_x-goog-api-key"], "doc_url": "https://ai.google.dev/docs"},
    {"provider_key": "ollama_local", "display_name": "Ollama Private Self-Hosted AI", "category": "AI", "auth_type": "API_KEY", "suggested_base_url": "http://localhost:11434/api", "required_credential_fields": [], "doc_url": "https://ollama.com"},

    # Maps
    {"provider_key": "google_maps", "display_name": "Google Maps Platform", "category": "MAPS", "auth_type": "CUSTOM_HEADER", "suggested_base_url": "https://maps.googleapis.com/maps/api", "required_credential_fields": ["api_key"], "doc_url": "https://developers.google.com/maps"},
    {"provider_key": "mapbox", "display_name": "Mapbox Navigation & Geocoding", "category": "MAPS", "auth_type": "API_KEY", "suggested_base_url": "https://api.mapbox.com", "required_credential_fields": ["api_key"], "doc_url": "https://docs.mapbox.com"},


    # Academic & Government Portals (National Digital Infrastructure)
    {"provider_key": "digilocker", "display_name": "DigiLocker National Document Ledger", "category": "GOV_PORTAL", "auth_type": "OAUTH2", "suggested_base_url": "https://api.digitallocker.gov.in/public/oauth2/1", "required_credential_fields": ["client_id", "client_secret", "org_id"], "doc_url": "https://partners.digitallocker.gov.in/"},
    {"provider_key": "abc_nad", "display_name": "Academic Bank of Credits (ABC / NAD)", "category": "GOV_PORTAL", "auth_type": "BEARER", "suggested_base_url": "https://api.abc.gov.in/v2", "required_credential_fields": ["token", "institution_code"], "doc_url": "https://www.abc.gov.in/"},
    {"provider_key": "ndl_india", "display_name": "National Digital Library of India (NDLI)", "category": "GOV_PORTAL", "auth_type": "API_KEY", "suggested_base_url": "https://ndl.iitkgp.ac.in/api/v1", "required_credential_fields": ["api_key"], "doc_url": "https://ndl.iitkgp.ac.in/"},
    {"provider_key": "uidai_ekyc", "display_name": "UIDAI Aadhaar e-KYC Verification", "category": "GOV_PORTAL", "auth_type": "CUSTOM_HEADER", "suggested_base_url": "https://auth.uidai.gov.in/2.5", "required_credential_fields": ["header_x-uidai-auth", "sub_aua_code"], "doc_url": "https://uidai.gov.in/"},

    # OTP
    {"provider_key": "custom_otp", "display_name": "Custom Dynamic OTP Gateway", "category": "OTP", "auth_type": "API_KEY", "suggested_base_url": "https://api.otp-service.internal", "required_credential_fields": ["api_key"], "doc_url": "https://myeducation.in/docs/otp"}
]

class UniversalProviderRegistry:
    @staticmethod
    def get_all_templates() -> List[Dict[str, Any]]:
        return TEMPLATES

    @staticmethod
    def find_template(provider_key: str) -> Optional[Dict[str, Any]]:
        for t in TEMPLATES:
            if t["provider_key"] == provider_key:
                return t
        return None
