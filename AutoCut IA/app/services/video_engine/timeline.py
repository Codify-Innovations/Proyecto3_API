def generate_timeline(clips, style_cfg):
    """
    Genera un timeline SEGURO donde cada clip tiene su duración exacta,
    sin acumulación de tiempo.
    """

    duration = style_cfg.get("duration", 3)  # duración por imagen

    out = []

    for c in clips:
        item = {
            "clip": c,
            "duration": duration,     # 🔥 duración fija por clip
            "zoom_intensity": style_cfg.get("zoom_intensity", 0),
            "use_shake": style_cfg.get("shake", False),

            # NO USAMOS ESTO PORQUE GENERA ERRORES VISUALES
            "flash": False,
            "aberration": False,
            "blur": False,

            # NO USAMOS TRANSICIONES PORQUE CAMBIAN DURACIÓN REAL
            "transition": None
        }

        out.append(item)

    return out
