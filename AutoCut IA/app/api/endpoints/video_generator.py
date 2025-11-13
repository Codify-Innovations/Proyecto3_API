from fastapi import APIRouter, HTTPException
from app.schemas.video_schema import VideoRequest
from app.services.video_service import generate_video  # ✅ ruta correcta

router = APIRouter()

@router.post("/generate-multiple")
async def generate_multiple(request: VideoRequest):
    """🎬 Genera un video con IA a partir de imágenes o clips."""
    try:
        result = generate_video(request)
        if not result or result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message", "Error generando el video."))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
