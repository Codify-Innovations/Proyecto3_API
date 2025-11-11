from fastapi import FastAPI
from app.api.endpoints import predict, analyze
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api/predict", tags=["Predicción"])
app.include_router(analyze.router, prefix="/api", tags=["Análisis Multimedia"])


@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
