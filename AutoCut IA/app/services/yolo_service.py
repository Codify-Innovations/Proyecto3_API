from ultralytics import YOLO
from PIL import Image
import torch
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)



logger.info("Cargando modelo YOLOv8 para detección de autos...")
yolo_model = YOLO("yolov8x.pt")

CROPS_DIR = os.path.join("app", "static", "crops")
os.makedirs(CROPS_DIR, exist_ok=True)


def detectar_auto(image: Image.Image):
    """
    Detecta el auto principal en la imagen usando YOLOv8,
    devuelve el recorte (PIL.Image) y guarda una copia en disco.
    """
    try:
        logger.debug("Ejecutando modelo YOLOv8 sobre la imagen.")
        results = yolo_model(image, verbose=False)
        detections = results[0].boxes

        car_boxes = []
        for box in detections:
            cls = int(box.cls[0])
            label = results[0].names[cls]
            logger.debug(f"Objeto detectado: {label}")

            if label in ["car", "truck", "bus", "motorbike"]:
                logger.debug(f"Vehículo identificado: {label}")
                car_boxes.append(box.xyxy[0])

        if not car_boxes:
            logger.warning("No se detectó ningún vehículo en la imagen.")
            raise ValueError("No se detectó ningún vehículo en la imagen.")

        areas = [(b[2] - b[0]) * (b[3] - b[1]) for b in car_boxes]
        best_box = car_boxes[areas.index(max(areas))]

        margin = 30
        x1, y1, x2, y2 = map(int, best_box)
        cropped_image = image.crop((
            max(0, x1 - margin),
            max(0, y1 - margin),
            min(image.width, x2 + margin),
            min(image.height, y2 + margin)
        ))

        return cropped_image

    except Exception as e:
        logger.error(f"❌ Error en detección YOLO: {str(e)}", exc_info=True)
        raise
