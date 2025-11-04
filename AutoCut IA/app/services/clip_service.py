from io import BytesIO
from PIL import Image
import requests
import torch
from app.core.model_loader import model, processor, df, labels

def predict_auto(image_url: str = None, image_bytes: bytes = None):
    if not image_url and not image_bytes:
        raise ValueError("Debes enviar una URL o una imagen válida.")

    # Cargar imagen desde URL o bytes
    if image_url:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Procesar con CLIP
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)

    # Obtener predicción más probable
    best_idx = torch.argmax(probs[0]).item()
    best_score = probs[0][best_idx].item()
    auto_info = df.iloc[best_idx]

    return {
        "marca": str(auto_info.get("marca", "Desconocida")),
        "modelo": str(auto_info.get("modelo", "Desconocido")),
        "año": str(auto_info.get("año", "Desconocido")),
        "descripcion": str(auto_info.get("descripcion", "Desconocida")),
        "confianza": round(best_score, 3)
    }
