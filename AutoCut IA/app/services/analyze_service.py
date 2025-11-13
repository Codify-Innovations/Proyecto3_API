import cv2
import numpy as np
import librosa
import tempfile
import os
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
import moviepy.editor as mp

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def convert_types(obj):
    if isinstance(obj, (np.float32, np.float64, np.int32, np.int64)):
        return float(obj)
    if isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_types(v) for v in obj]
    return obj

def interpret_metric(value, ideal, warning):
    if value is None:
        return "N/A"
    if value >= ideal:
        return "Excelente"
    elif value >= warning:
        return "Aceptable"
    return "Deficiente"

def clean(v):
    if v is None:
        return None
    return round(float(v), 2)

def build_response(tipo, score, quality_label, metrics, suggestions):
    return convert_types({
        "type": tipo,
        "score": round(float(score), 2),
        "quality_label": quality_label,
        "metrics": metrics,
        "suggestions": suggestions
    })

def analyze_image(path):
    image = Image.open(path).convert("RGB")
    np_img = np.array(image)
    height, width = np_img.shape[:2]
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)

    brightness = clean(np.mean(gray) / 255)
    contrast = clean(gray.std() / 128)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    sharpness_norm = clean(min(sharpness / 1000, 1))

    texts = [
        "imagen profesional",
        "imagen borrosa",
        "imagen bien iluminada",
        "imagen mal iluminada"
    ]
    inputs = processor(text=texts, images=image, return_tensors="pt", padding=True).to(device)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1).cpu().detach().numpy()[0]

    ia_value = clean(probs[0] + probs[2])
    stability = clean(1.0)

    score = ((brightness + contrast + sharpness_norm + ia_value) / 4) * 100

    metrics = {
        "resolucion": f"{width}x{height}",
        "iluminacion": {"valor": brightness, "evaluacion": interpret_metric(brightness, 0.75, 0.4)},
        "contraste": {"valor": contrast, "evaluacion": interpret_metric(contrast, 0.8, 0.5)},
        "nitidez": {"valor": sharpness_norm, "evaluacion": interpret_metric(sharpness_norm, 0.7, 0.4)},
        "estabilidad": {"valor": stability, "evaluacion": "Excelente"},
        "ia_score": {"valor": ia_value, "evaluacion": interpret_metric(ia_value, 0.8, 0.5)}
    }

    suggestions = []
    if brightness < 0.75:
        suggestions.append(
            "La iluminación es baja; usar una fuente de luz más uniforme o grabar en un entorno más iluminado ayudará a que se capturen mejor los detalles de la imagen."
        )
    if sharpness_norm < 0.7:
        suggestions.append(
            "La nitidez es limitada; mantener la cámara estable o asegurar un enfoque más preciso permitirá obtener una imagen más clara y definida."
        )
    if contrast < 0.5:
        suggestions.append(
            "El contraste es reducido; ajustar la exposición o mejorar las condiciones de luz facilitará una separación más clara entre zonas oscuras y claras."
        )
    if ia_value < 0.6:
        suggestions.append(
            "La IA detecta baja coherencia visual; mejorar iluminación y estabilidad puede ayudar a obtener resultados más precisos."
        )

    return build_response("image", score, "Evaluación visual completa", metrics, suggestions)

def analyze_audio(path):
    y, sr = librosa.load(path, sr=None)

    rms = clean(np.mean(librosa.feature.rms(y=y)))
    zcr = clean(np.mean(librosa.feature.zero_crossing_rate(y)))
    centroid = clean(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))

    claridad = clean(1 - zcr)
    ruido = clean(1 - rms)
    balance = clean(min(centroid / 5000, 1))

    audio_score = clean((claridad + (1 - ruido) + balance) / 3)

    metrics = {
        "claridad": {"valor": claridad, "evaluacion": interpret_metric(claridad, 0.8, 0.5)},
        "ruido": {"valor": ruido, "evaluacion": interpret_metric(ruido, 0.7, 0.4)},
        "balance": {"valor": balance, "evaluacion": interpret_metric(balance, 0.75, 0.5)},
        "audio_score": {"valor": audio_score, "evaluacion": interpret_metric(audio_score, 0.8, 0.5)}
    }

    suggestions = []
    if claridad < 0.7:
        suggestions.append(
            "El audio presenta baja claridad; hablar más cerca del micrófono o grabar en un espacio con menos eco mejorará la definición sonora."
        )
    if ruido > 0.4:
        suggestions.append(
            "Se detecta ruido de fondo; grabar en un entorno más silencioso o aplicar reducción de ruido mejorará la limpieza del audio."
        )
    if balance < 0.5:
        suggestions.append(
            "El balance de frecuencias no es uniforme; ajustar graves y agudos permitirá obtener un sonido más equilibrado."
        )

    return {"metrics": metrics, "score": audio_score * 100, "suggestions": suggestions}

def analyze_video(path):
    cap = cv2.VideoCapture(path)
    fps = clean(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_ids = np.linspace(0, total_frames - 1, num=min(30, total_frames)).astype(int)

    brightness_list = []
    stability_list = []
    prev_gray = None

    for fid in frame_ids:
        cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
        ret, frame = cap.read()
        if not ret: continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness_list.append(clean(np.mean(gray) / 255))

        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None,
                                                0.5, 3, 15, 3, 5, 1.2, 0)
            motion = np.mean(np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2))
            stability_list.append(clean(1 - min(motion / 10, 1)))

        prev_gray = gray

    cap.release()

    brightness = clean(np.mean(brightness_list))
    stability = clean(np.mean(stability_list))
    fluidez = clean(min(fps / 30, 1))

    audio_metrics = {}
    audio_score = 0.6

    try:
        with mp.VideoFileClip(path) as clip:
            if clip.audio:
                audio_path = tempfile.mktemp(suffix=".wav")
                clip.audio.write_audiofile(audio_path, logger=None)
                audio_data = analyze_audio(audio_path)
                audio_metrics = audio_data["metrics"]
                audio_score = clean(audio_data["score"] / 100)
                os.remove(audio_path)
    except:
        pass

    final_score = ((brightness + stability + fluidez) / 3 * 0.6 + audio_score * 0.4) * 100

    metrics = {
        "resolucion": f"{width}x{height}",
        "iluminacion": {"valor": brightness, "evaluacion": interpret_metric(brightness, 0.75, 0.4)},
        "estabilidad": {"valor": stability, "evaluacion": interpret_metric(stability, 0.7, 0.5)},
        "fps": fps,
        "fluidez": {"valor": fluidez, "evaluacion": interpret_metric(fluidez, 0.9, 0.7)},
        **audio_metrics
    }

    suggestions = []
    if brightness < 0.75:
        suggestions.append(
            "El video tiene iluminación limitada; grabar con una fuente de luz más fuerte o más cercana ayuda a mejorar la claridad visual."
        )
    if stability < 0.7:
        suggestions.append(
            "Se detecta movimiento entre cuadros; usar un trípode o apoyar la cámara permitirá obtener un video más estable."
        )
    if fluidez < 0.9:
        suggestions.append(
            "La fluidez del video es baja; grabar a más FPS generará un movimiento más suave y natural."
        )
    if audio_score < 0.7:
        suggestions.append(
            "El audio del video puede mejorarse; grabar en un entorno silencioso o usar un micrófono externo incrementará la calidad final."
        )

    return build_response("video", final_score, "Evaluación audiovisual completa", metrics, suggestions)
