import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change_this_key'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
