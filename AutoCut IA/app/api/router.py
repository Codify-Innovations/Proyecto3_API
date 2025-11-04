from fastapi import APIRouter
from app.api.endpoints import predict

api_router = APIRouter()

# Prefijos y tags por módulo
api_router.include_router(predict.router, prefix="/api/predict", tags=["Predicción"])