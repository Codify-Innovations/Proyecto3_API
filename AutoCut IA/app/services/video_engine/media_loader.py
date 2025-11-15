import requests
import numpy as np
from io import BytesIO
from PIL import Image
from moviepy.editor import ImageClip, VideoFileClip
from .utils import debug


def load_media_list(urls, duration):
    clips = []
    resolutions = []

    for url in urls:
        debug(f"Descargando: {url}")

        # 📌 Detectar si es VIDEO
        if url.lower().endswith((".mp4", ".mov", ".webm", ".avi", ".mkv")):
            temp_path = "temp_video.mp4"

            r = requests.get(url, stream=True)
            with open(temp_path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)

            clip = VideoFileClip(temp_path)
            clips.append(clip)
            resolutions.append((clip.w, clip.h))
            continue

        # 📌 Si es IMAGEN
        r = requests.get(url)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        frame = np.array(img)

        clip = ImageClip(frame).set_duration(duration)
        clips.append(clip)
        resolutions.append((img.width, img.height))

    debug(f"Total media cargada: {len(clips)}")
    return clips, resolutions



from moviepy.editor import ImageClip, CompositeVideoClip


def prepare_all_clips(clips, target_w, target_h):
    """
    Ajusta imágenes y videos manteniendo proporción SIN RECORTAR.
    Agrega barras negras (letterbox/pillarbox) y centra la imagen.
    """

    processed = []

    for c in clips:
        w, h = c.w, c.h

        # 📌 Escala manteniendo proporción exacta
        scale = min(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        # 📌 Redimensionar sin estirar
        resized = c.resize((new_w, new_h))

        # 📌 Fondo negro tamaño final exacto
        background = ImageClip(
            np.zeros((target_h, target_w, 3), dtype=np.uint8)
        ).set_duration(c.duration)

        # 📌 Overlay limpio y centrado
        final = CompositeVideoClip(
            [background, resized.set_position(("center", "center"))],
            size=(target_w, target_h)
        ).set_duration(c.duration)

        processed.append(final)

    return processed
