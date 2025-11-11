from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.clip_service import predict_auto
from app.schemas.auto_schema import PredictRequest, PredictResponse

router = APIRouter()

@router.post("/", response_model=PredictResponse)
async def predict_endpoint(body: PredictRequest):
    """
    Predice el auto a partir de una URL de imagen.
    """
    try:
        if not body.image_url:
            raise HTTPException(status_code=400, detail="Debe proporcionar una URL de imagen válida.")
        try:
            result = predict_auto(image_url=body.image_url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error durante la predicción: {str(e)}")

        if not result or "marca" not in result:
            raise HTTPException(status_code=500, detail="No se obtuvo una predicción válida del modelo.")

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
