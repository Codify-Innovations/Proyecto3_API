from transformers import CLIPProcessor, CLIPModel
import pandas as pd
from app.core.config import settings

print("🚗 Loading CLIP model and dataset...")

try:
    model = CLIPModel.from_pretrained(settings.MODEL_NAME)
    processor = CLIPProcessor.from_pretrained(settings.MODEL_NAME)
except Exception as e:
    raise RuntimeError(f"❌ Error loading CLIP model or processor: {str(e)}")

try:
    df = pd.read_excel(settings.EXCEL_PATH)
    df.columns = df.columns.str.lower()

    required_cols = {"brand", "model", "year", "category"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"The Excel file is missing required columns: {', '.join(missing)}")

    df["full_phrase"] = df.apply(
        lambda row: (
            f"a photo of a {row['category']} car: "
            f"{row['brand']} {row['model']} ({int(row['year'])}), "
        ),
        axis=1
    )

    df["full_phrase"] = df["full_phrase"].str.lower().str.strip()
    labels = df["full_phrase"].dropna().tolist()

except FileNotFoundError:
    raise RuntimeError("❌ The Excel file was not found at the configured path.")
except ValueError as ve:
    raise RuntimeError(f"❌ Excel data error: {str(ve)}")
except Exception as e:
    raise RuntimeError(f"❌ Error loading or processing dataset: {str(e)}")

print(f"✅ CLIP model and dataset loaded successfully ({len(labels)} labels available).")
