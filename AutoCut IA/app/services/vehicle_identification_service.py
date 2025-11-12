# app/services/ai_identification_service.py
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import requests
from app.services.yolo_service import detectar_auto
from app.services.gemini_service import GeminiService

def predict_auto(image_url: str):
    """
    Detecta el vehículo en la imagen con YOLO y lo identifica con Gemini.
    Retorna la marca, modelo, año y color.
    """
    if not image_url:
        raise ValueError("Debe proporcionar una URL de imagen válida.")

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        raise ValueError(f"Error al descargar o procesar la imagen: {str(e)}")

    try:
        cropped_image = detectar_auto(image)
    except Exception as e:
        raise ValueError(f"Error al detectar vehículo: {str(e)}")

    buf = BytesIO()
    cropped_image.save(buf, format="JPEG")
    buf.seek(0)

    try:
        gemini = GeminiService()
        result = gemini.identify_vehicle(image_url=image_url)
    except Exception as e:
        raise ValueError(f"Error al analizar con Gemini: {str(e)}")

    if "error" in result:
        raise ValueError(result["error"])

    return {
        "marca": result.get("brand", "Desconocida"),
        "modelo": result.get("model", "Desconocido"),
        "año": result.get("year", "Desconocido"),
        "color": result.get("color", "Desconocido"),
        "categoria": result.get("category", "Desconocido")
    }
