import cv2, numpy as np, librosa, tempfile, shutil, os
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
import moviepy.editor as mp

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def interpret_metric(value: float, ideal: float, warning: float) -> str:
    if value >= ideal:
        return "Excelente"
    elif value >= warning:
        return "Aceptable"
    else:
        return "Deficiente"


def analyze_image(path):
    image = Image.open(path).convert("RGB")
    np_img = np.array(image)
    height, width = np_img.shape[:2]
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)

    brightness = np.mean(gray) / 255
    contrast = gray.std() / 128
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    sharpness_norm = min(sharpness / 1000, 1)
    noise_level = np.var(cv2.GaussianBlur(gray, (3,3), 0) - gray) / 100  

    texts = [
        "una imagen de alta calidad, bien iluminada y enfocada",
        "una imagen borrosa o con poca luz",
        "una foto de baja resolución",
        "una fotografía profesional y nítida",
        "una imagen sobreexpuesta o mal iluminada"
    ]
    inputs = processor(text=texts, images=image, return_tensors="pt", padding=True).to(device)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1).detach().cpu().numpy()[0]
    ia_score = probs[0] + probs[3] 

    total_score = round(((brightness + contrast + sharpness_norm + ia_score) / 4) * 100, 2)

    metric_reference = {
        "resolucion": f"{width}x{height}",
        "iluminacion": {"valor": round(brightness, 2), "ideal": "≥ 0.75", "evaluacion": interpret_metric(brightness, 0.75, 0.4)},
        "contraste": {"valor": round(contrast, 2), "ideal": "≥ 0.8", "evaluacion": interpret_metric(contrast, 0.8, 0.5)},
        "nitidez": {"valor": round(sharpness_norm, 2), "ideal": "≥ 0.7", "evaluacion": interpret_metric(sharpness_norm, 0.7, 0.4)},
        "ruido": {"valor": round(noise_level, 2), "ideal": "≤ 0.3", "evaluacion": "Buena" if noise_level < 0.3 else "Alta (ruidosa)"},
        "ia_score": {"valor": round(float(ia_score), 2), "ideal": "≥ 0.8", "evaluacion": interpret_metric(ia_score, 0.8, 0.5)},
    }

    suggestions = []
    if brightness < 0.75:
        suggestions.append("La iluminación es insuficiente. Usa luz natural o ajusta exposición.")
    if contrast < 0.8:
        suggestions.append("El contraste es bajo. Ajusta niveles o curvas para más profundidad.")
    if sharpness_norm < 0.7:
        suggestions.append("La imagen está poco nítida. Verifica el enfoque o la cámara.")
    if noise_level > 0.3:
        suggestions.append("La imagen tiene ruido visible. Usa reducción de ruido o ISO más bajo.")
    if ia_score < 0.8:
        suggestions.append("No parece profesional. Mejora composición, luz o resolución.")
    if not suggestions:
        suggestions.append("La imagen tiene una calidad excelente, cercana al 100%. ¡Excelente trabajo!")

    label = (
        "Excelente calidad visual." if total_score > 85 else
        "Buena calidad general." if total_score > 70 else
        "Calidad media, requiere ajustes." if total_score > 50 else
        "Baja calidad visual."
    )

    return {
        "type": "image",
        "score": total_score,
        "quality_label": label,
        "metrics": metric_reference,
        "suggestions": suggestions
    }


def analyze_video(path):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_ids = np.linspace(0, total_frames - 1, num=min(60, total_frames)).astype(int)
    brightness_list, stability_list = [], []
    prev_gray = None

    for fid in frame_ids:
        cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness_list.append(np.mean(gray) / 255)
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            motion = np.mean(np.sqrt(flow[...,0]**2 + flow[...,1]**2))
            stability_list.append(1 - min(motion / 10, 1))
        prev_gray = gray

    cap.release()

    brightness = np.mean(brightness_list) if brightness_list else 0.5
    stability = np.mean(stability_list) if stability_list else 0.5
    fluidez = min(fps / 30, 1)
    resolution = min((width * height) / (1920 * 1080), 1)
    score_visual = (brightness + stability + fluidez + resolution) / 4

    total_score = round(score_visual * 100, 2)

    metric_reference = {
        "resolucion": f"{width}x{height}",
        "fps": round(fps, 1),
        "iluminacion": {"valor": round(brightness, 2), "ideal": "≥ 0.75", "evaluacion": interpret_metric(brightness, 0.75, 0.4)},
        "estabilidad": {"valor": round(stability, 2), "ideal": "≥ 0.7", "evaluacion": interpret_metric(stability, 0.7, 0.5)},
        "fluidez": {"valor": round(fluidez, 2), "ideal": "≥ 0.9", "evaluacion": interpret_metric(fluidez, 0.9, 0.7)},
    }

    suggestions = []
    if brightness < 0.75:
        suggestions.append("Aumenta la iluminación para una mejor exposición.")
    if stability < 0.7:
        suggestions.append("Reduce vibraciones usando trípode o estabilizador.")
    if fluidez < 0.9:
        suggestions.append("Graba a más FPS para una reproducción fluida.")
    if not suggestions:
        suggestions.append("El video cumple con todos los parámetros de alta calidad. ¡Excelente trabajo!")

    label = (
        "Excelente calidad audiovisual." if total_score > 85 else
        "Buena calidad general." if total_score > 70 else
        "Calidad media." if total_score > 50 else
        "Baja calidad audiovisual."
    )

    return {"type": "video", "score": total_score, "quality_label": label, "metrics": metric_reference, "suggestions": suggestions}


def analyze_audio(path):
    y, sr = librosa.load(path, sr=None)
    rms = np.mean(librosa.feature.rms(y=y))
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    spec_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    claridad = 1 - zcr
    balance = min(spec_centroid / 5000, 1)
    ruido = max(0, min(1, 1 - rms))
    score = round(((claridad + (1 - ruido) + balance) / 3) * 100, 2)

    metric_reference = {
        "claridad": {"valor": round(claridad, 2), "ideal": "≥ 0.8", "evaluacion": interpret_metric(claridad, 0.8, 0.5)},
        "ruido": {"valor": round(ruido, 2), "ideal": "≤ 0.4", "evaluacion": "Buena" if ruido < 0.4 else "Alta (ruidosa)"},
        "balance": {"valor": round(balance, 2), "ideal": "≥ 0.75", "evaluacion": interpret_metric(balance, 0.75, 0.5)},
    }

    suggestions = []
    if claridad < 0.8:
        suggestions.append("Aumenta la claridad evitando distorsión o ecos.")
    if ruido > 0.4:
        suggestions.append("Reduce el ruido de fondo o usa un micrófono aislado.")
    if balance < 0.75:
        suggestions.append("Ajusta el balance de frecuencias para un sonido más natural.")
    if not suggestions:
        suggestions.append("El audio presenta una calidad excelente, cercana al 100%.")

    label = (
        "Audio excelente." if score > 85 else
        "Audio bueno con margen de mejora." if score > 70 else
        "Audio aceptable con ruido." if score > 50 else
        "Audio deficiente."
    )

    return {"type": "audio", "score": score, "quality_label": label, "metrics": metric_reference, "suggestions": suggestions}