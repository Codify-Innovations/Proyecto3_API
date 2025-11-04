from transformers import CLIPProcessor, CLIPModel
import pandas as pd
from app.core.config import settings

print("🚗 Cargando modelo CLIP y datos...")

# === Modelo ===
model = CLIPModel.from_pretrained(settings.MODEL_NAME)
processor = CLIPProcessor.from_pretrained(settings.MODEL_NAME)

# === Dataset ===
df = pd.read_excel(settings.EXCEL_PATH)
df.columns = df.columns.str.lower()
df["frase_completa"] = df.apply(
    lambda row: f"{row['marca']} {row['modelo']} {row['año']} {row['descripcion']}",
    axis=1
)
labels = df["frase_completa"].dropna().tolist()
