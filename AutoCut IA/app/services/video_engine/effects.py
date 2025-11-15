from moviepy.editor import vfx
from PIL import Image, ImageFilter
import numpy as np


def apply_flash(clip, intensity=0.3):
    """
    Flash suave, sin quemar la imagen.
    """
    return clip.fx(vfx.lum_contrast, lum=8, contrast=3)


def apply_aberration(clip, shift=2):
    """
    Aberración cromática suave y estética.
    """
    def effect(get_frame, t):
        f = get_frame(t).copy()

        r = np.roll(f[:, :, 0], shift, axis=1)
        b = np.roll(f[:, :, 2], -shift, axis=1)

        f[:, :, 0] = r
        f[:, :, 2] = b
        return f

    return clip.fl(effect)


def apply_blur(clip, level=1):
    """
    Blur suave para transiciones.
    """
    radius = level * 1.2

    def blur_frame(frame):
        img = Image.fromarray(frame)
        img = img.filter(ImageFilter.GaussianBlur(radius=radius))
        return np.array(img)

    return clip.fl_image(blur_frame)
