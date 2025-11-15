import os
from cloudinary.uploader import upload as cloudinary_upload
from .video_engine.media_loader import load_media_list, prepare_all_clips
from .video_engine.resolution import choose_project_resolution
from .video_engine.analyzer import analyze_style
from .video_engine.engine import build_video


def generate_video_from_request(request):
    urls = request.image_urls
    style = request.style
    duration = request.duration
    music_url = request.music_url

    # 1) Cargar imágenes/videos
    clips, resolutions = load_media_list(urls, duration)

    # 2) Elegir resolución base
    w, h = choose_project_resolution(resolutions)

    # 3) 🔥 Asegurar que SIEMPRE sean números
    try:
        w = int(w)
        h = int(h)
    except:
        w = 1920
        h = 1080

    # 4) Preparar clips con resolución corregida
    prepared = prepare_all_clips(clips, w, h)

    # 5) Analizar estilo (NADA que recorte ni dañe la imagen)
    style_cfg = analyze_style(style)

    # 6) Construir video final
    return build_video(prepared, style_cfg, music_url)
