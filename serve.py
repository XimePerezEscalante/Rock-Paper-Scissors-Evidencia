"""
POST /predict  -> recibe una imagen (campo "image") y devuelve la clase predicha

Como usarlo:
    .venv/bin/uvicorn serve:app --port 8000
"""
import io
import numpy as np
import tensorflow as tf

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, ImageOps, UnidentifiedImageError

from preprocess import CLASS_NAMES
from predict import load_trained_model
from train_cnn import IMG_SIZE

# Contraataque que le gana a cada clase para  "ganarle" al usuario
COUNTER_MOVE = {"rock": "paper", "paper": "scissors", "scissors": "rock"}

app = FastAPI(title="Rock Paper Scissors CNN")
model = load_trained_model()


def to_tensor(data: bytes):
    # PIL soporta JPG, PNG y WEBP; exif_transpose corrige la rotación de las fotos del celular
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    img = np.asarray(img, dtype=np.float32) / 255.0
    return tf.image.resize(img, (IMG_SIZE, IMG_SIZE))


@app.get("/health")
def health():
    return {"status": "ok", "classes": CLASS_NAMES}


@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    try:
        tensor = to_tensor(await image.read())
    except UnidentifiedImageError:
        raise HTTPException(status_code=415, detail="No se pudo leer la imagen.")

    probs = model.predict(tf.expand_dims(tensor, 0), verbose=0)[0]
    label = CLASS_NAMES[int(np.argmax(probs))]
    return {
        "label": label,
        "confidence": float(np.max(probs)),
        "probabilities": {name: float(p) for name, p in zip(CLASS_NAMES, probs)},
        "counter": COUNTER_MOVE[label],
    }
