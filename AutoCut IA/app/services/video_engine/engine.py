from moviepy.editor import concatenate_videoclips, AudioFileClip
from .timeline import generate_timeline
from .motion import apply_zoom, apply_shake
from .audio import pick_music
from .bars import apply_bars
from .grain import apply_grain
from .fade import apply_fade
from .colorgrading import (
    apply_vibrance,
    apply_contrast,
    apply_dark,
    apply_warm,
    apply_bw,
    apply_soft_glow,
)
from .utils import debug


def apply_style_overrides(clip, preset):

    if preset.get("vibrance"):
        clip = apply_vibrance(clip)

    if preset.get("contrast_boost"):
        clip = apply_contrast(clip)

    if preset.get("dark"):
        clip = apply_dark(clip)

    if preset.get("warm"):
        clip = apply_warm(clip)

    if preset.get("bw"):
        clip = apply_bw(clip)

    if preset.get("soft_glow"):
        clip = apply_soft_glow(clip)

    if preset.get("bars"):
        clip = apply_bars(clip)

    if preset.get("grain"):
        clip = apply_grain(clip)

    if preset.get("fade"):
        clip = apply_fade(clip)

    return clip



def build_video(prepared_clips, style_cfg, music_url):
    timeline = generate_timeline(prepared_clips, style_cfg)
    processed = []

    # APLICAR EFECTOS Y DURACIONES
    for item in timeline:
        clip = item["clip"].set_duration(item["duration"])

        if item.get("zoom_intensity"):
            clip = apply_zoom(clip, item["zoom_intensity"])

        clip = apply_style_overrides(clip, style_cfg)
        processed.append(clip)

    # ENSAMBLAR VIDEO FINAL
    video = concatenate_videoclips(processed, method="compose")

    # ===============================
    # 🔥 APLICAR MÚSICA (FINAL FIX)
    # ===============================
    music = pick_music(music_url, style_cfg)
    debug(f"Usando música: {music}")

    try:
        audio = AudioFileClip(music)

        # ⭐ CORTAR EL AUDIO EXACTAMENTE A LA DURACIÓN DEL VIDEO
        audio = audio.subclip(0, video.duration)

        # ⭐ APLICAR AUDIO RECORTADO
        video = video.set_audio(audio.volumex(0.85))

        debug("[AUDIO] Música aplicada correctamente.")

    except Exception as e:
        debug(f"[AUDIO ERROR] No se pudo cargar el MP3: {e}")

    return video
