import pandas as pd
from app.core.config import settings


class DropdownsService:
    def __init__(self):
        self._cache = None

    def _load_excel(self):
        df = pd.read_excel(settings.EXCEL_PATH)
        df.columns = df.columns.str.lower().str.strip()
        return df

    def get_dropdowns(self):
        if self._cache is not None:
            return dict(self._cache)

        df = self._load_excel()
        required_cols = {"brand", "model", "category"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"El Excel debe contener las columnas: {', '.join(required_cols)}")

        df = df.dropna(subset=["brand", "model", "category"]).drop_duplicates()

        result = {}
        for _, row in df.iterrows():
            brand = str(row["brand"]).strip()
            model = str(row["model"]).strip()
            category = str(row["category"]).strip()

            if brand not in result:
                result[brand] = {"modelos": set(), "categorias": set()}

            result[brand]["modelos"].add(model)
            result[brand]["categorias"].add(category)

        self._cache = {
            brand: {
                "modelos": sorted(list(data["modelos"])),
                "categorias": sorted(list(data["categorias"]))
            }
            for brand, data in result.items()
        }

        return dict(self._cache)

    def reload(self):
        self._cache = None
        return self.get_dropdowns()


dropdowns_service = DropdownsService()
