from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.dropdowns_service import dropdowns_service

router = APIRouter()

@router.get("/", summary="Obtiene los valores únicos para los dropdowns (marca, modelo, categoría)")
async def get_dropdowns():
    """
    Retorna listas únicas de marcas, modelos y categorías
    obtenidas desde el archivo Excel.
    """
    try:
        result = dropdowns_service.get_dropdowns()
        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron datos en el archivo.")
        return JSONResponse(content=result)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="El archivo Excel no fue encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los dropdowns: {str(e)}")


@router.post("/reload", summary="Recarga los datos desde el Excel")
async def reload_dropdowns():
    """
    Recarga manualmente los datos desde el Excel, actualizando las listas en memoria.
    """
    try:
        result = dropdowns_service.reload()
        return JSONResponse(content={"message": "Datos recargados correctamente", "data": result})

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="El archivo Excel no fue encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recargar los dropdowns: {str(e)}")
