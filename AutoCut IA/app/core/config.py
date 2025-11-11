import os

class Settings:
    PROJECT_NAME: str = " IA API"
    VERSION: str = "1.0.0"
    MODEL_NAME: str = os.getenv("MODEL_NAME", "openai/clip-vit-base-patch32")
    EXCEL_PATH: str = os.getenv("EXCEL_PATH", "model_prueba.xlsx")

settings = Settings()
