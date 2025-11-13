import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    PROJECT_NAME: str = " IA API"
    VERSION: str = "1.0.0"
    MODEL_NAME: str = os.getenv("MODEL_NAME", "openai/clip-vit-base-patch32")

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
settings = Settings()
