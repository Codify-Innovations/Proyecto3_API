from .utils import debug

def analyze_style(style: str):
    style = (style or "").lower()

    presets = {
        "cinematic": {
            "bars": True,
            "cinema_warm": True,
            "grain": True,
            "soft_darkness": True,
            "contrast_boost": False,
            "color_pop": False,
            "soft_glow": False,
            "bw": False,
            "transition": "fade",
            "duration": 3,
            "default_music": "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Kai_Engel/Irsens_Tale/Kai_Engel_-_07_-_Wake_Up.mp3"
        },
        "trap": {
            "soft_darkness": True,
            "grain": True,
            "fade": True,
            "contrast_boost": False,
            "soft_glow": False,
            "color_pop": False,
            "zoom_intensity": 0.12,
            "transition": "fade",
            "duration": 3.5,
            "default_music": "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/UncountedLost/Single/UncountedLost_-_Horror_Trap_beat.mp3"
        },
        "minimal": {
            "bw": True,
            "fade": True,
            "grain": False,
            "contrast_boost": False,
            "color_pop": False,
            "soft_glow": False,
            "zoom_intensity": 0.05,
            "transition": "fade",
            "duration": 3,
            "default_music": "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Purrple_Cat/Singles/Purrple_Cat_-_Life_Adventures.mp3"
        },
    }

    preset = presets.get(style, presets["showcase"])
    debug(f"[STYLE] preset aplicado '{style}': {preset}")
    return preset
