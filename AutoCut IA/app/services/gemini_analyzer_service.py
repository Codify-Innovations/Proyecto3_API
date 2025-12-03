from google import genai
from PIL import Image
from io import BytesIO
import requests
import json
import logging
from app.core.config import settings


class GeminiContentAnalyzerService:

    logger = logging.getLogger(__name__)

    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            self.logger.error("GOOGLE_API_KEY no está configurada.")
            raise ValueError("Falta GOOGLE_API_KEY en el archivo .env o variables de entorno.")

        self.logger.info("Inicializando cliente de Gemini con la API Key configurada.")
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    # ============================================================
    # ANALIZAR IMAGEN / VIDEO / AUDIO DESDE URL
    # ============================================================
    def analyze(self, media_url: str, media_type: str):
        """
        media_type: 'image', 'video', 'audio'
        media_url: URL pública (Cloudinary u otra)
        """

        prompt = self._build_prompt(media_type)

        try:
            # Descargar archivo desde URL
            self.logger.info(f"Descargando archivo desde URL: {media_url}")
            response_file = requests.get(media_url, timeout=15)
            response_file.raise_for_status()

            file_bytes = response_file.content

            # Si el tipo es imagen, convertir a PIL.Image
            if media_type == "image":
                try:
                    image = Image.open(BytesIO(file_bytes))
                except Exception:
                    self.logger.error("El archivo no es una imagen válida para análisis de imagen.")
                    raise ValueError("El URL no contiene una imagen válida.")
                
                gemini_input = image

            else:
                # Videos y audios se envían como bytes
                gemini_input = file_bytes

            # Llamada a Gemini
            gemini_response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, gemini_input]
            )

            text = gemini_response.text.strip()

            # Limpieza de bloques markdown
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            # Intentar parsear a JSON
            try:
                parsed = json.loads(text)
                self.logger.info("JSON válido recibido desde Gemini.")
            except json.JSONDecodeError:
                self.logger.warning("Gemini devolvió texto no JSON. Devolviendo raw_response.")
                parsed = {"raw_response": text}

            self.logger.info(f"Resultado análisis multimedia: {parsed}")
            return parsed

        except Exception as e:
            self.logger.exception("Error inesperado durante el análisis multimedia.")
            return {"error": str(e)}

    # ============================================================
    # PROMPT
    # ============================================================
    def _build_prompt(self, media_type: str):
        return f"""
Eres un auditor experto en calidad multimedia. Analiza el/la {media_type} proporcionado(a)
y produce exclusivamente un objeto JSON con la siguiente estructura exacta:

{{
  "type": "{media_type}",
  "score": número entre 0 y 100,
  "quality_label": "Evaluación visual completa",
  "metrics": {{
    "resolucion": "WIDTHxHEIGHT",
    "iluminacion": {{
      "valor": número entre 0 y 1,
      "evaluacion": "Excelente" | "Aceptable" | "Deficiente"
    }},
    "contraste": {{
      "valor": número entre 0 y 1,
      "evaluacion": "Excelente" | "Aceptable" | "Deficiente"
    }},
    "nitidez": {{
      "valor": número entre 0 y 1,
      "evaluacion": "Excelente" | "Aceptable" | "Deficiente"
    }},
    "estabilidad": {{
      "valor": número entre 0 y 1,
      "evaluacion": "Excelente" | "Aceptable" | "Deficiente"
    }},
    "ia_score": {{
      "valor": número entre 0 y 1,
      "evaluacion": "Excelente" | "Aceptable" | "Deficiente"
    }}
  }},
  "suggestions": ["sugerencia detallada 1", "sugerencia detallada 2"]
}}

REQUISITOS DE GENERACIÓN:
- TODO debe estar completamente en español.
- Debes seguir la estructura EXACTA del JSON, sin agregar ni eliminar claves.
- No incluyas texto fuera del objeto JSON.
- Extrae "resolucion" de la imagen o video si es posible.
- Estima perceptualmente:
  iluminación (brightness), contraste, nitidez (sharpness), estabilidad (motion stability),
  y ia_score (coherencia visual o calidad perceptual).
- Todas las métricas deben estar entre 0.0 y 1.0.
- El "score" es un valor entre 0 y 100 que representa la calidad global.
- Las sugerencias deben ser entre 1 y 3 elementos, cada una redactada en español,
  con un nivel de detalle moderado (1 a 3 líneas), explicando cómo mejorar de manera práctica y clara.
- No uses viñetas ni formato especial. Solo texto plano dentro de cada sugerencia.
"""
