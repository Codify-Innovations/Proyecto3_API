# app/routes/content_quality_analyzer.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.gemini_analyzer_service import GeminiContentAnalyzerService

router = APIRouter()
gemini_service = GeminiContentAnalyzerService()

# ============================
# Request Schema
# ============================
class AnalyzeURLRequest(BaseModel):
    url: str


@router.post("/analyze/{media_type}")
async def analyze_content(media_type: str, body: AnalyzeURLRequest):
    """
    Analiza calidad de imagen, audio o video usando Gemini 2.0 Flash.
    
    media_type debe ser uno de:
    - image
    - video
    - audio

    Recibe un JSON:
    {
        "url": "https://res.cloudinary.com/.../archivo.jpg"
    }
    """

    if media_type not in ["image", "video", "audio"]:
        raise HTTPException(
            status_code=400, 
            detail="media_type debe ser: image, video o audio."
        )

    if not body.url:
        raise HTTPException(
            status_code=400,
            detail="Debe proporcionar una URL pública válida."
        )

    try:
        # Analizar directamente desde URL (Cloudinary)
        result = gemini_service.analyze(body.url, media_type)

        # return JSONResponse(content=result)
        return JSONResponse(content={
            "status": "success",
            "data": result
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )
