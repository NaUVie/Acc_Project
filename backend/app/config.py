import os
from dotenv import load_dotenv

# Load environmental variables from .env file
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
