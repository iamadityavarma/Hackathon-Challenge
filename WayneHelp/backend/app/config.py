# import os


# class Config:

#     SECRET_KEY = "988b0156d0d668df515aab41f6923fc41d5faccb8ec7f4d2822ee4a38e866558"
#     basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#     # Database URI with absolute path
#     SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "app.db")}'
#     OPENAI_API_KEY = "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"
#     ANTHROPIC_API_KEY = "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"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = "585306bb1e573f7d90dff6c679f957bbfc74db67bf6842ecfae59150ca37b452"
#     # MAIL_SERVER = 'smtp.gmail.com'
#     # MAIL_PORT = 587
#     # MAIL_USE_TLS = True
#     # MAIL_USERNAME = 'your_email@gmail.com'
#     # MAIL_PASSWORD = 'your_email_password'

import os
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"
    )
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
