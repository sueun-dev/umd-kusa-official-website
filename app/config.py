# app/config.py
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()  # Load environment variables from .env file


class Config:
    # Flask configuration
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Upload settings
    # Absolute path ensures the uploads folder is correctly referenced
    UPLOAD_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "uploads"
    )
    MAX_CONTENT_LENGTH = 12 * 1024 * 1024  # 12 MB
    ALLOWED_EXTENSIONS = {
        "pdf",
        "docx",
        "png",
        "jpeg",
        "jpg",
        "gif",
        "bmp",
        "svg",
        "txt",
        "rtf",
        "csv",
        "html",
    }

    # Authentication settings
    USERNAME = os.getenv("UPLOAD_USERNAME", "admin")
    UPLOAD_PASSWORD_HASH = generate_password_hash(
        os.getenv("UPLOAD_PASSWORD", "password"), method="pbkdf2:sha256"
    )

    # Login attempt settings
    MAX_ATTEMPTS = 7
    BLOCK_TIME = 24 * 60 * 60  # 24 hours in seconds
