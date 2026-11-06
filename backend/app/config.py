import os
from dotenv import load_dotenv

from pathlib import Path

# Load environmental variables from .env file (check backend/.env as well as current dir)
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/acc_academy")
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "127.0.0.1")

import urllib.parse

cloudinary_url = os.getenv("CLOUDINARY_URL", "")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

if cloudinary_url and "cloudinary://" in cloudinary_url:
    try:
        parsed = urllib.parse.urlparse(cloudinary_url)
        if parsed.hostname:
            CLOUDINARY_CLOUD_NAME = parsed.hostname
        if parsed.username:
            CLOUDINARY_API_KEY = parsed.username
        if parsed.password:
            CLOUDINARY_API_SECRET = parsed.password
    except Exception as e:
        print(f"Error parsing CLOUDINARY_URL: {e}")

CLOUDINARY_FOLDER = os.getenv("CLOUDINARY_FOLDER", "Acc Demo")

# VNPay Sandbox Configuration
VNPAY_TMN_CODE = os.getenv("VNPAY_TMN_CODE", "2QXUI4J4")
VNPAY_HASH_SECRET = os.getenv("VNPAY_HASH_SECRET", "KASJDKASJDKASJDKASJDKASJDKASJDKA")
VNPAY_PAYMENT_URL = os.getenv("VNPAY_PAYMENT_URL", "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html")
VNPAY_RETURN_URL = os.getenv("VNPAY_RETURN_URL", "http://localhost:5173/payment/vnpay-return")

# Resend Email API settings
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "ACC Academy <onboarding@resend.dev>")

# Email notification settings (SMTP)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
ADMIN_NOTIFICATION_EMAIL = os.getenv("ADMIN_NOTIFICATION_EMAIL", "")
