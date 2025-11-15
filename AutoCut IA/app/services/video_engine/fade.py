from moviepy.editor import vfx

def apply_fade(clip, duration=0.6):
    return clip.fx(vfx.fadein, duration).fx(vfx.fadeout, duration)
