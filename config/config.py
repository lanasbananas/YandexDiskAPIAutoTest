from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    API_TOKEN = os.getenv("API_TOKEN")

    @staticmethod
    def validate():
        if not Config.API_TOKEN:
            raise ValueError("API_TOKEN not set")
        if not Config.BASE_URL:
            raise ValueError("BASE_URL not set")