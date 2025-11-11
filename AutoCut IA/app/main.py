from fastapi import FastAPI
from app.api.endpoints import dropdowns_endpoint, predict
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",   
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],          
)

app.include_router(predict.router, prefix="/api/predict", tags=["Predicción"])
app.include_router(dropdowns_endpoint.router, prefix="/api/dropdowns", tags=["Dropdowns"])


@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
