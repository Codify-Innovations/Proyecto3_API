from moviepy.editor import vfx
import numpy as np


def apply_zoom(clip, intensity=0.15):
    """
    Zoom suave tipo 'punch-in'
    """
    factor = 1 + float(intensity)
    return clip.fx(vfx.resize, factor)


def apply_shake(clip, max_shift=6):
    """
    Shake estabilizado sin destruir bordes.
    """
    def shake_frame(frame):
        h, w, _ = frame.shape
        dx = np.random.randint(-max_shift, max_shift)
        dy = np.random.randint(-max_shift, max_shift)

        M = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        return shifted

    return clip.fl_image(shake_frame)
