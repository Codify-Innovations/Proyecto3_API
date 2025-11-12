# app/routes/vehicle_identification.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.vehicle_identification_service import predict_auto
from app.schemas.auto_schema import PredictRequest, PredictResponse

router = APIRouter()

@router.post("/", response_model=PredictResponse)
async def predict_endpoint(body: PredictRequest):
    """
    Predice la información del vehículo (marca, modelo, año, color)
    usando detección YOLO + análisis Gemini.
    """
    if not body.image_url:
        raise HTTPException(status_code=400, detail="Debe proporcionar una URL de imagen válida.")

    try:
        result = predict_auto(body.image_url)
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
