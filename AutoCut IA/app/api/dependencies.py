from fastapi import UploadFile, HTTPException, Depends
from app.core.config import settings

async def validate_file_size(
    file: UploadFile,
    config=Depends(lambda: settings)
) -> UploadFile:

    if file.size and file.size > config.max_file_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo excede el límite de {config.MAX_FILE_SIZE_MB} MB"
        )

    return file
