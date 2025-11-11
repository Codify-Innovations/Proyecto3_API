from io import BytesIO
from PIL import Image, UnidentifiedImageError
import requests
import torch
from app.core.model_loader import model, processor, df, labels
from app.services.yolo_service import detectar_auto  # 👈 Importar YOLO

def predict_auto(image_url: str):
    """
    Predice la información del auto a partir de una URL de imagen.

    - Descarga la imagen desde la URL.
    - Usa el modelo CLIP para compararla con las descripciones del dataset.
    - Retorna la marca, modelo, año, descripción y nivel de confianza.
    """

    if not image_url:
        raise ValueError("Debe proporcionar una URL de imagen válida.")

    try:
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.MissingSchema:
        raise ValueError("La URL proporcionada no tiene un formato válido (falta http/https).")
    except requests.exceptions.ConnectionError:
        raise ValueError("No se pudo conectar al servidor de la URL.")
    except requests.exceptions.Timeout:
        raise ValueError("La solicitud a la URL de imagen excedió el tiempo de espera.")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error al obtener la imagen desde la URL: {str(e)}")

    try:
        image = Image.open(BytesIO(response.content)).convert("RGB")
    except UnidentifiedImageError:
        raise ValueError("El archivo descargado no es una imagen válida o está corrupto.")
    except Exception as e:
        raise ValueError(f"Error al procesar la imagen: {str(e)}")

    try:
        cropped_image = detectar_auto(image)
    except ValueError as e:
        raise ValueError(str(e))

    try:
        inputs = processor(text=labels, images=cropped_image, return_tensors="pt", padding=True)
        outputs = model(**inputs)

        temperature = 0.7
        probs = torch.nn.functional.softmax(outputs.logits_per_image / temperature, dim=1)

        sorted_probs, indices = torch.sort(probs[0], descending=True)
        best_idx = indices[0].item()
        best_score = sorted_probs[0].item()
        second_best = sorted_probs[1].item()
        relative_confidence = (best_score - second_best) * 100 

        auto_info = df.iloc[best_idx]

    except Exception as e:
        raise ValueError(f"Error durante el procesamiento del modelo CLIP: {str(e)}")

    try:
        best_idx = torch.argmax(probs[0]).item()
        best_score = probs[0][best_idx].item()
        auto_info = df.iloc[best_idx]
    except Exception as e:
        raise ValueError(f"Error al obtener la predicción: {str(e)}")

    try:
      return {
            "marca": str(auto_info.get("brand", "Desconocida")),
            "modelo": str(auto_info.get("model", "Desconocido")),
            "año": str(auto_info.get("year", "Desconocido")),
            "descripcion": str(auto_info.get("description", "Desconocida")), 
            "categoria": str(auto_info.get("category", "Desconocida")),
        }


    except Exception as e:
        raise ValueError(f"Error al construir la respuesta final: {str(e)}")