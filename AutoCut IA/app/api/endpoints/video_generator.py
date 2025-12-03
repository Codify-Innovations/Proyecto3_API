from fastapi import APIRouter, HTTPException
from app.schemas.video_schema import VideoRequest
from app.services.video_service import generate_video_from_request
import os
from cloudinary.uploader import upload as cloudinary_upload
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate-edit")
async def generate_edit(request: VideoRequest):
    try:
        video = generate_video_from_request(request)

        output = "output_video.mp4"

        video.write_videofile(
            output,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )

        # Subir a Cloudinary
        result = cloudinary_upload(output, folder="generated_videos", resource_type="video")

        # Limpiar archivos temporales
        if os.path.exists(output):
            os.remove(output)

        return {"status": "success", "video_url": result.get("secure_url")}

    except Exception as e:
        logger.error(f"Error generating video: {str(e)}", exc_info=True)
        raise HTTPException(500, str(e))
