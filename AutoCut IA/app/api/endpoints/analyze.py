from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.analyze_service import analyze_image, analyze_video, analyze_audio
import tempfile, shutil, os

router = APIRouter(tags=["Media Analysis"])

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Recibe un archivo multimedia (imagen, video o audio)
    y ejecuta el análisis con IA (imagen, video o audio).
    """
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    ctype = file.content_type.lower()
    result = {"error": "Tipo de archivo no soportado. Solo se aceptan imágenes, videos o audios."}

    try:
        if "image" in ctype:
            result = analyze_image(tmp_path)
        elif "video" in ctype:
            result = analyze_video(tmp_path)
        elif "audio" in ctype:
            result = analyze_audio(tmp_path)
    except Exception as e:
        result = {"error": f"Error procesando el archivo: {str(e)}"}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return JSONResponse(content={"status": "success", "data": result})
