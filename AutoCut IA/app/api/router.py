from fastapi import APIRouter
from app.api.endpoints import predict, video_generator


api_router = APIRouter()

# Prefijos y tags por módulo
api_router.include_router(predict.router, prefix="/api/predict", tags=["Predicción"])
router.include_router(video_generator.router, tags=["Video Generator"])
