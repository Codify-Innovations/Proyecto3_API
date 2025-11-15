from moviepy.editor import ImageClip, CompositeVideoClip
import numpy as np


def choose_project_resolution(style_config=None):
    return {
        "width": 1280,   # int
        "height": 720    # int
    }


    processed = []

    for c in clips:
        # dimensiones originales del clip
        w, h = c.w, c.h

        # 🔥 Escalar manteniendo proporción AL 100%
        scale = min(target_w / w, target_h / h)

        new_w = int(w * scale)
        new_h = int(h * scale)

        # Imagen/video escalado SIN deformarse
        resized = c.resize((new_w, new_h))

        # 🔳 Fondo negro EXACTO del tamaño esperado
        background = ImageClip(
            np.zeros((target_h, target_w, 3), dtype=np.uint8)
        ).set_duration(c.duration)

        # 💎 Composición limpia: fondo + clip centrado
        final = CompositeVideoClip(
            [
                background,
                resized.set_position(("center", "center"))
            ],
            size=(target_w, target_h)
        ).set_duration(c.duration)

        processed.append(final)

    return processed
