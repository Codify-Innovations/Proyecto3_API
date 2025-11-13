import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    PROJECT_NAME: str = " IA API"
    VERSION: str = "1.0.0"
    MODEL_NAME: str = os.getenv("MODEL_NAME", "openai/clip-vit-base-patch32")

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")
    CLOUDINARY_SECURE: bool = os.getenv("CLOUDINARY_SECURE", "True").lower() == "true"
settings = Settings()
