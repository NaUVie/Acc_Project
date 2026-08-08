import os
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/acc_academy")
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "127.0.0.1")

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "dzhtookky")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "846798972285995")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "g0DsZ-CX-NAoX0vHPcdH3idiAEs")
CLOUDINARY_FOLDER = os.getenv("CLOUDINARY_FOLDER", "Acc Demo")
