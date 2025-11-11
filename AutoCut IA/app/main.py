import os
import sys
import multiprocessing

# ============================================================
# 🧩 FIX: Cargar entorno virtual (.venv) correctamente
# ============================================================
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
venv_path = os.path.join(project_root, ".venv", "Lib", "site-packages")

if not os.path.exists(venv_path):
    # Si no está al mismo nivel, sube un nivel adicional (por seguridad)
    venv_path = os.path.abspath(os.path.join(project_root, "..", ".venv", "Lib", "site-packages"))

if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

print(f"✅ Librerías cargadas desde entorno virtual: {venv_path}")

# ============================================================
# 🚀 CONFIGURACIÓN FASTAPI
# ============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import predict, video_generator
from app.core.config import settings
import cloudinary

# Evita errores en Windows con multiprocessing
multiprocessing.freeze_support()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="🎬 Microservicio IA de AutoCut: Predicción e IA de generación de video"
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
# 🔒 MIDDLEWARE CORS
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir luego a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🔗 RUTAS PRINCIPALES
# ============================================================
app.include_router(predict.router, prefix="/api/predict", tags=["Predicción"])
app.include_router(video_generator.router, prefix="/api/video", tags=["Generador de Video"])

# ============================================================
# 🏠 ENDPOINT DE PRUEBA
# ============================================================
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "🚗 AutoCut IA API funcionando correctamente 🚀",
        "endpoints": ["/api/predict", "/api/video"],
    }
