from pydantic import BaseModel

class PredictResponse(BaseModel):
    marca: str
    modelo: str
    año: str
    descripcion: str
    confianza: float

    class Config:
        from_attributes = True
class PredictRequest(BaseModel):
    image_url: str