import numpy as np

def apply_grain(clip, strength=25):
    def grain_frame(frame):
        noise = np.random.randint(-strength, strength, frame.shape, dtype=np.int16)
        noisy = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return noisy

    return clip.fl_image(grain_frame)
