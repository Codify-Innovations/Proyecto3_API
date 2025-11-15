from google import genai
from PIL import Image
from io import BytesIO
import requests
import os
import json
from app.core.config import settings


class GeminiService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("⚠️ Falta GOOGLE_API_KEY en el archivo .env o variables de entorno.")
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    def identify_vehicle(self, image_url: str):
        """
        Identifica marca, modelo, año y color aproximado de un vehículo
        a partir de una imagen usando el modelo  gemini-2.0-flash.
        """
        # prompt = (
        #     "You are an automotive identification expert. "
        #     "Analyze the provided car image and return ONLY a valid JSON object with the following keys: "
        #     "`brand`, `model`, `year`, and `color`. "
        #     "The color should be the dominant visible color of the car's body. "
        #     "Return only the JSON object, without markdown or text outside the JSON."
        # )
        prompt = (
            "You are an expert automotive analyst. "
            "Analyze the provided car image and return ONLY a valid JSON object "
            "with the following keys: `brand`, `model`, `year`, `color`, and `category`. "
            "The `category` must represent the general automotive type or segment of the car, "
            "choosing from this list of common categories: "
                "['hypercar', 'supercar', 'sports', 'JDM', 'muscle', 'classic', 'luxury', "
                "'SUV', 'sedan', 'pickup', 'off-road', 'compact', 'convertible', 'wagon', 'electric', 'van', 'concept']. "
            "Base the classification on the vehicle’s design, style, and context. "
            "For the `year`, return ONLY the **single most probable production year** "
            "of the vehicle visible in the image (not a range of years). "
            "The color should be the dominant visible color of the body. "
            "Return ONLY a valid JSON object with those keys, without any markdown, explanation, or text outside the JSON."
        )

        try:
            img_data = requests.get(image_url, timeout=10).content
            image = Image.open(BytesIO(img_data))

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, image],
            )

            text = response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                print("⚠️ No se pudo parsear JSON, respuesta cruda:", text)
                data = {"raw_response": text}

            print("✅ Resultado IA:", data)
            return data

        except Exception as e:
            print(f"❌ Error al analizar vehículo con Gemini: {e}")
            return {"error": str(e)}
