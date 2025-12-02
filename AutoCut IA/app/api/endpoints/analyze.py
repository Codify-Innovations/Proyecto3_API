from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse
import tempfile, shutil, os

from app.services.analyze_service import analyze_image, analyze_video, analyze_audio
from app.api.dependencies import validate_file_size

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = Depends(validate_file_size)):

    if not file:
        return JSONResponse(status_code=400, content={"status": "error", "message": "No se envió ningún archivo."})

    if not any(t in file.content_type for t in ["image", "video", "audio"]):
        return JSONResponse(status_code=400, content={"status": "error", "message": "Formato no soportado."})

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        if "image" in file.content_type:
            result = analyze_image(tmp_path)
        elif "video" in file.content_type:
            result = analyze_video(tmp_path)
        elif "audio" in file.content_type:
            result = analyze_audio(tmp_path)
        else:
            raise ValueError("Formato no soportado.")

        return JSONResponse(content={"status": "success", "data": result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Error interno: {str(e)}"})

    finally:
        os.remove(tmp_path)
