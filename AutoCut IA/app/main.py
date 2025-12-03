import os
import sys
import multiprocessing
from fastapi import FastAPI
from app.api.endpoints import analyze,vehicle_identificacion,gemini_analyze
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import video_generator
from app.core.config import settings
from app.core.logging_config import *
import cloudinary

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
venv_path = os.path.join(project_root, ".venv", "Lib", "site-packages")

if not os.path.exists(venv_path):
    venv_path = os.path.abspath(os.path.join(project_root, "..", ".venv", "Lib", "site-packages"))

if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

print(f"✅ Librerías cargadas desde entorno virtual: {venv_path}")

multiprocessing.freeze_support()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="🎬 Microservicio IA de AutoCut: Predicción, Análisis y Generación de Video"
)

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=settings.CLOUDINARY_SECURE,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_generator.router, prefix="/api/video", tags=["Generador de Video"])
app.include_router(analyze.router, prefix="/api", tags=["Análisis Multimedia"])
app.include_router(vehicle_identificacion.router, prefix="/api/vehicle_identification", tags=["Vehicle Identification"])
app.include_router(gemini_analyze.router, prefix="/api/gemini", tags=["Gemini Analyze"])

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "AutoCut IA API funcionando correctamente",
        "endpoints": [
            "/api/predict",
            "/api/video",
            "/api"
        ],
    }
