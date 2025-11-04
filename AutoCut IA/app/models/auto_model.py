from pydantic import BaseModel

class AutoModel(BaseModel):
    marca: str
    modelo: str
    año: str
    descripcion: str
    confianza: float

    class Config:
        orm_mode = True
