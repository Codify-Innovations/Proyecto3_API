from fastapi import FastAPI
from app.api.endpoints import predict
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.include_router(predict.router, prefix="/api/predict", tags=["Predicción"])

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
