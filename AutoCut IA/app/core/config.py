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

    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 10
    
settings = Settings()
