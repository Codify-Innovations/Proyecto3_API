import sys
import os

# Agregar ruta donde está TRELLIS
sys.path.append(os.path.abspath("../TRELLIS"))

from trellis.pipelines import TrellisImageTo3DPipeline
from trellis.utils import postprocessing_utils
from PIL import Image

def generate_3d_car(image_path: str, seed: int = 1):
    print("🔄 Cargando modelo TRELLIS...")
    pipeline = TrellisImageTo3DPipeline.from_pretrained("microsoft/TRELLIS-image-large")
    pipeline.cuda()
    print("✅ Modelo cargado correctamente")

    img = Image.open(image_path)
    outputs = pipeline.run(img, seed=seed)

    glb_path = "auto_model.glb"
    glb = postprocessing_utils.to_glb(outputs['gaussian'][0], outputs['mesh'][0])
    glb.export(glb_path)

    print(f"🚗 Modelo 3D generado: {glb_path}")
    return glb_path
