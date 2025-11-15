import os
import sys
import multiprocessing

# ============================================================
# 🧩 FIX: Cargar entorno virtual (.venv) correctamente
# ============================================================
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
venv_path = os.path.join(project_root, ".venv", "Lib", "site-packages")

if not os.path.exists(venv_path):
    venv_path = os.path.abspath(os.path.join(project_root, "..", ".venv", "Lib", "site-packages"))

if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

print(f"✅ Librerías cargadas desde entorno virtual: {venv_path}")

# ============================================================
# 🚀 CONFIGURACIÓN FASTAPI
# ============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import cloudinary

# Routers originales (correctos)
from app.api.endpoints.predict import router as predict_router
from app.api.endpoints.video_generator import router as video_router

# Router de análisis multimedia (el que tus compañeros usan)
from app.api.endpoints.analyze import router as analyze_router

from app.core.config import settings

multiprocessing.freeze_support()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="🎬 Microservicio IA de AutoCut: Predicción, Análisis y Generación de Video"
)

# ============================================================
# ☁️ CONFIGURACIÓN CLOUDINARY
# ============================================================
cloudinary.config(
    cloud_name="dzejxb251",
    api_key="772823312336243",
    api_secret="6SXovJsGxxNjgWaWADkT01kHIB8",
    secure=True,
)

# ============================================================
# 🔒 MIDDLEWARE CORS (solo una vez)
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🔗 RUTAS PRINCIPALES (ya sin duplicación)
# ============================================================
# Rutas ORIGINALMENTE usadas por tu equipo
app.include_router(predict_router, prefix="/api/predict", tags=["Predicción"])
app.include_router(analyze_router, prefix="/api", tags=["Análisis Multimedia"])

# RUTA que tú necesitas para el generador de video IA
app.include_router(video_router, prefix="/api/video", tags=["Generador de Video"])

# ============================================================
# 🏠 ENDPOINT DE PRUEBA
# ============================================================
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "🚗 AutoCut IA API funcionando correctamente 🚀",
        "endpoints": [
            "/api/predict",
            "/api/video",
            "/api"
        ],
    }
