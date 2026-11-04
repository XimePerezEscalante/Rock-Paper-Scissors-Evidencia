"""
Como probar el modelo:

    python predict.py # evalúa con el conjunto de test
    python predict.py foto.png  # clasifica imágenes individuales
"""
import sys
import numpy as np
import tensorflow as tf

from pathlib import Path
from tensorflow import keras

from preprocess import CLASS_NAMES, load_datasets
from train_cnn import IMG_SIZE, build_model, confusion_matrix, prepare

# Rutas
MODEL_PATH = Path(__file__).parent / "rps_cnn.keras"
WEIGHTS_PATH = Path(__file__).parent / "rps_cnn.weights.h5"

# Cargar el modelo
def load_trained_model():
    # El .keras trae arquitectura + pesos; si no existe, se reconstruye la red y se cargan solo los pesos
    if MODEL_PATH.exists():
        return keras.models.load_model(MODEL_PATH)
    model = build_model()
    model.load_weights(WEIGHTS_PATH)
    return model

# Cargar la imagen
def load_image(filepath):
    raw_img = tf.io.read_file(str(filepath))
    img = tf.image.decode_image(raw_img, channels=3, expand_animations=False)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return tf.image.resize(img, (IMG_SIZE, IMG_SIZE))

# Funcion para hacer la prediccion
def predict_images(model, filepaths):
    batch = tf.stack([load_image(p) for p in filepaths])
    probs = model.predict(batch, verbose=0)
    for path, p in zip(filepaths, probs):
        scores = "  ".join(f"{name}: {prob:.2%}" for name, prob in zip(CLASS_NAMES, p))
        print(f"{path} -> {CLASS_NAMES[int(np.argmax(p))]}   ({scores})")


if __name__ == "__main__":
    model = load_trained_model()

    if len(sys.argv) > 1:
        predict_images(model, sys.argv[1:])
    else:
        # Mismo SEED que en el entrenamiento, así que es exactamente el mismo conjunto de test
        _, _, test_ds = load_datasets()
        test_ds = prepare(test_ds)
        test_loss, test_acc = model.evaluate(test_ds, verbose=0)
        print(f"Test loss: {test_loss:.4f}  |  Test accuracy: {test_acc:.4f}")
        confusion_matrix(model, test_ds)
