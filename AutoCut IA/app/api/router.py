from fastapi import APIRouter
from app.api.endpoints import dropdowns_endpoint, predict

api_router = APIRouter()

# Prefijos y tags por módulo
api_router.include_router(predict.router, prefix="/api/predict", tags=["Predicción"])


api_router.include_router(dropdowns_endpoint.router, prefix="/api/dropdowns", tags=["Dropdowns"])

