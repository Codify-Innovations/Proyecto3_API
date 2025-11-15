from moviepy.editor import CompositeVideoClip, vfx


# 🌐 Zoom elegante entre clips
def soft_zoom_transition(c1, c2):
    d = 0.35
    zoomed = c1.fx(vfx.resize, 1.15).set_end(c1.duration + d)
    next_clip = c2.set_start(c1.duration)

    return CompositeVideoClip([zoomed, next_clip])


# ⚡ Flash elegante (NO quema la imagen)
def soft_flash_transition(c1, c2):
    d = 0.20
    flash = c1.fx(vfx.lum_contrast, lum=60, contrast=10).set_duration(d)

    return CompositeVideoClip([
        c1,
        flash.set_start(c1.duration),
        c2.set_start(c1.duration + d)
    ])


# 🎬 Fundido suave profesional
def fade_transition(c1, c2):
    return c1.crossfadeout(0.4).set_end(c1.duration).set_start(0) \
        .set_audio(c2.audio)
