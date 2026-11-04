import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

from PIL import Image
from pathlib import Path

IMAGES_PATH = Path(__file__).parent / "images"
CLASS_NAMES = ["rock", "paper", "scissors"]

# Rutas a las carpetas de cada clase
path_rock = IMAGES_PATH / "rock"
path_paper = IMAGES_PATH / "paper"
path_scissors = IMAGES_PATH / "scissors"

# Constantes para la Division del Dataset
SEED = 42 # 42
VAL_FRACTION = 0.15
TEST_FRACTION = 0.15

# Cargar las imagenes desde las carpetas locales
def load_image(filepath, label):
    raw_img = tf.io.read_file(filepath)
    img_tensor_int = tf.image.decode_png(raw_img, channels=3)
    img_tensor_flt = tf.image.convert_image_dtype(img_tensor_int, tf.float32)
    return img_tensor_flt, label

# Cargar el Dataset
def load_datasets():
    # Se asigna una etiqueta: 0 = rock; 1 = paper; 2 = scissors
    filepaths, labels = [], []
    for label, class_name in enumerate(CLASS_NAMES):
        files = sorted(str(p) for p in (IMAGES_PATH / class_name).glob("*.png"))
        filepaths += files
        labels += [label] * len(files)

    rng = np.random.default_rng(SEED)
    order = rng.permutation(len(filepaths))
    filepaths = np.array(filepaths)[order]
    labels = np.array(labels)[order]

    # Dividir el dataset
    n_test = int(len(filepaths) * TEST_FRACTION)
    n_val = int(len(filepaths) * VAL_FRACTION)

    def make_ds(start, end):
        ds = tf.data.Dataset.from_tensor_slices((filepaths[start:end], labels[start:end]))
        return ds.map(load_image, num_parallel_calls=tf.data.AUTOTUNE)

    test_ds = make_ds(0, n_test)
    val_ds = make_ds(n_test, n_test + n_val)
    train_ds = make_ds(n_test + n_val, len(filepaths))
    return train_ds, val_ds, test_ds

