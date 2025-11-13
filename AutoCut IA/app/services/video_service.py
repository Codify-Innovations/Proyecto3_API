import os
import sys
import importlib.util

# ================================================================
# 🧩 FIX FINAL DEFINITIVO - Cargar MoviePy en Windows correctamente
# ================================================================

# Ruta al entorno virtual actual (AutoCut IA/.venv)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
venv_path = os.path.join(base_dir, ".venv", "Lib", "site-packages")

# Forzar solo ese entorno virtual (sin subir más niveles)
if venv_path not in sys.path and os.path.exists(venv_path):
    sys.path.insert(0, venv_path)

print(f"🧩 Cargando MoviePy desde entorno virtual fijo: {venv_path}")

# ================================================================
# Intentar importar MoviePy (modo normal)
# ================================================================
try:
    from moviepy.editor import (
        ImageSequenceClip,
        VideoFileClip,
        concatenate_videoclips,
        vfx,
        ColorClip,
        CompositeVideoClip,
    )
    print("✅ MoviePy importado correctamente desde entorno actual.")
except ModuleNotFoundError as e:
    print(f"⚠️ No se pudo importar MoviePy directamente: {e}")
    print("🔄 Intentando carga manual desde el entorno forzado...")
    spec = importlib.util.find_spec("moviepy.editor")
    if spec is None:
        raise ImportError(f"❌ MoviePy no se encontró en {venv_path}. Verifica la instalación con: pip install moviepy")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals().update({
        "ImageSequenceClip": module.ImageSequenceClip,
        "VideoFileClip": module.VideoFileClip,
        "concatenate_videoclips": module.concatenate_videoclips,
        "vfx": module.vfx,
        "ColorClip": module.ColorClip,
        "CompositeVideoClip": module.CompositeVideoClip,
    })
    print("✅ MoviePy cargado correctamente (modo manual).")


except ModuleNotFoundError:
    print("⚠️ MoviePy no se encontró en sys.path, intentando carga manual...")
    spec = importlib.util.find_spec("moviepy.editor")
    if spec is None:
        raise ImportError(f"❌ No se pudo cargar MoviePy desde: {venv_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals().update({
        "ImageSequenceClip": module.ImageSequenceClip,
        "VideoFileClip": module.VideoFileClip,
        "concatenate_videoclips": module.concatenate_videoclips,
        "vfx": module.vfx,
        "ColorClip": module.ColorClip,
        "CompositeVideoClip": module.CompositeVideoClip,
    })
    print("✅ MoviePy cargado correctamente (modo manual).")


# ================================================================
# ☁️ IMPORTS PRINCIPALES Y CONFIGURACIÓN
# ================================================================
from cloudinary.uploader import upload as cloudinary_upload
from PIL import Image
from io import BytesIO
import numpy as np
import requests


# ================================================================
# 🎨 FUNCIONES AUXILIARES DE ESTILO
# ================================================================
def apply_style(clip, style: str):
    """Aplica un filtro visual dependiendo del estilo elegido."""
    style = (style or "").lower()
    print(f"🎨 Aplicando estilo: {style}")

    try:
        if style == "dynamic":
            clip = clip.fx(vfx.speedx, 1.5)
            clip = clip.fx(vfx.lum_contrast, lum=10, contrast=30)

        elif style == "cinematic":
            clip = clip.fx(vfx.colorx, 0.9)
            h, w = clip.h, clip.w
            bar_height = int(h * 0.12)
            top_bar = ColorClip(size=(w, bar_height), color=(0, 0, 0)).set_duration(clip.duration)
            bottom_bar = top_bar.set_position(("center", h - bar_height))
            clip = CompositeVideoClip([clip, top_bar.set_position(("center", 0)), bottom_bar])

        elif style == "minimal":
            clip = clip.fx(vfx.blackwhite)
            clip = clip.fx(vfx.fadein, 0.8).fx(vfx.fadeout, 0.8)

    except Exception as e:
        print(f"⚠️ Error aplicando estilo '{style}': {e}")

    return clip


# ================================================================
# 🎬 FUNCIÓN PRINCIPAL PARA GENERAR VIDEO
# ================================================================
def generate_video(request):
    """Procesa imágenes/videos, los combina y aplica el estilo solicitado."""
    try:
        clips = []
        duration = getattr(request, "duration", 2)
        print(f"📥 Procesando archivos multimedia (duración: {duration}s)...")

        # Iterar sobre URLs de imágenes o videos
        for i, url in enumerate(request.image_urls):
            print(f"🎞️ Archivo {i + 1}: {url}")
            lower_url = url.lower()

            # Si es un video
            if lower_url.endswith((".mp4", ".webm", ".mov", ".avi", ".mkv")):
                response = requests.get(url, stream=True)
                temp_path = f"temp_video_{i}.mp4"
                with open(temp_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                clip = VideoFileClip(temp_path).resize((1280, 720))
                clips.append(clip)

            # Si es una imagen
            elif lower_url.endswith((".jpg", ".jpeg", ".png", ".webp")):
                response = requests.get(url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content)).convert("RGB")
                    img = img.resize((1280, 720))
                    clips.append(ImageSequenceClip([np.array(img)], durations=[duration]))
                else:
                    print(f"⚠️ No se pudo descargar la imagen: {url}")

            else:
                print(f"⚠️ Tipo de archivo no soportado: {url}")

        if not clips:
            raise ValueError("No se pudieron obtener archivos válidos para generar el video.")

        # Aplicar estilos
        styled_clips = [apply_style(c, getattr(request, "style", "")) for c in clips]
        final_clip = concatenate_videoclips(styled_clips, method="compose")

        # Generar video final
        output_path = "output_video.mp4"
        final_clip.write_videofile(output_path, codec="libx264", fps=24, audio=False)

        # Subir a Cloudinary
        print("☁️ Subiendo video a Cloudinary...")
        upload_result = cloudinary_upload(
            output_path, folder="generated_videos", resource_type="video"
        )

        # Limpieza de recursos
        for clip in clips:
            clip.close()
        final_clip.close()
        os.remove(output_path)

        print("✅ Proceso completado correctamente")
        return {"status": "success", "video_url": upload_result.get("secure_url")}

    except Exception as e:
        print(f"❌ Error generando video: {e}")
        return {"status": "error", "message": str(e)}
