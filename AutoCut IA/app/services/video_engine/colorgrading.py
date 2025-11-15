from moviepy.editor import vfx
import numpy as np
from PIL import Image, ImageFilter


def apply_vibrance(clip):
    return clip.fx(vfx.lum_contrast, lum=5, contrast=10)


def apply_contrast(clip):
    return clip.fx(vfx.lum_contrast, lum=0, contrast=18)


def apply_dark(clip):
    return clip.fx(vfx.colorx, 0.90)


def apply_warm(clip):
    return clip.fx(vfx.colorx, 1.05)


def apply_bw(clip):
    return clip.fx(vfx.blackwhite)


def apply_soft_glow(clip):
    def glow_frame(frame):
        img = Image.fromarray(frame)
        blurred = img.filter(ImageFilter.GaussianBlur(radius=6))
        result = Image.blend(img, blurred, alpha=0.15)
        return np.array(result)
    return clip.fl_image(glow_frame)
