from moviepy.editor import ColorClip, CompositeVideoClip


def apply_bars(clip, bar_ratio=0.12):
    h, w = clip.h, clip.w
    bar_h = int(h * bar_ratio)

    top = ColorClip(size=(w, bar_h), color=(0, 0, 0)).set_duration(clip.duration)
    bottom = top.set_position(("center", h - bar_h))

    return CompositeVideoClip([clip, top.set_position(("center", 0)), bottom])