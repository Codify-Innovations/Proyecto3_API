from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.clip_service import predict_auto
from app.schemas.auto_schema import PredictResponse

router = APIRouter()

@router.post("/", response_model=PredictResponse)
async def predict_endpoint(image_url: str = Form(None), file: UploadFile = File(None)):
    """Predice el auto a partir de una URL o archivo de imagen."""
    try:
        image_bytes = await file.read() if file else None
        result = predict_auto(image_url=image_url, image_bytes=image_bytes)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
