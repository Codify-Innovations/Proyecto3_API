import requests
import os
from .utils import debug

TEMP_MUSIC_PATH = "temp_music.mp3"


def pick_music(music_url, style_cfg):
    """
    Descarga el MP3 si el usuario envía URL.
    Si no envía, retornamos la música interna según estilo.
    """

    # Si el usuario NO mandó música → usar música por defecto
    if not music_url:
        debug("[AUDIO] Usando música por defecto del estilo.")
        return style_cfg.get("default_music", "assets/music/default.mp3")

    try:
        debug(f"[AUDIO] Descargando música personalizada: {music_url}")

        r = requests.get(music_url, timeout=10)
        r.raise_for_status()

        # Guardar mp3 temporal
        with open(TEMP_MUSIC_PATH, "wb") as f:
            f.write(r.content)

        debug("[AUDIO] Música descargada correctamente.")
        return TEMP_MUSIC_PATH

    except Exception as e:
        debug(f"[ERROR AUDIO] No se pudo descargar música personalizada: {e}")
        return style_cfg.get("default_music", "assets/music/default.mp3")
