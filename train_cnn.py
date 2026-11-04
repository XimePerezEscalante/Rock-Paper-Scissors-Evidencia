import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from pathlib import Path
from tensorflow import keras
from tensorflow.keras import layers

from preprocess import CLASS_NAMES, SEED, load_datasets

OUTPUT_PATH = Path(__file__).parent
IMG_SIZE = 150
BATCH_SIZE = 32
EPOCHS = 30

tf.keras.utils.set_random_seed(SEED)


def prepare(ds, shuffle=False):
    # Reducir de 300x300 a 150x150 acelera mucho el entrenamiento sin perder la forma de la mano
    ds = ds.map(lambda img, label: (tf.image.resize(img, (IMG_SIZE, IMG_SIZE)), label),
                num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.cache()
    if shuffle:
        ds = ds.shuffle(1000, seed=SEED)
    return ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)


def build_model():
    # Aumento de datos: solo se aplica durante el entrenamiento
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.15),
        layers.RandomContrast(0.2),
    ], name="data_augmentation")

    model = keras.Sequential([
        keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        data_augmentation,

        layers.Conv2D(32, 3, padding="same", activation="relu"),
        layers.BatchNormalization(momentum=0.9),
        layers.MaxPooling2D(),

        layers.Conv2D(64, 3, padding="same", activation="relu"),
        layers.BatchNormalization(momentum=0.9),
        layers.MaxPooling2D(),

        layers.Conv2D(128, 3, padding="same", activation="relu"),
        layers.BatchNormalization(momentum=0.9),
        layers.MaxPooling2D(),

        layers.Conv2D(128, 3, padding="same", activation="relu"),
        layers.BatchNormalization(momentum=0.9),
        layers.MaxPooling2D(),

        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(len(CLASS_NAMES), activation="softmax"),
    ], name="rps_cnn")

    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    return model


def plot_history(history):
    f, axs = plt.subplots(1, 2, figsize=(12, 4))
    for ax, metric in zip(axs, ["loss", "accuracy"]):
        ax.plot(history.history[metric], label="train")
        ax.plot(history.history["val_" + metric], label="val")
        ax.set_title(metric)
        ax.set_xlabel("epoch")
        ax.legend()
    f.tight_layout()
    f.savefig(OUTPUT_PATH / "training_history.png")


def confusion_matrix(model, ds):
    y_true = np.concatenate([labels.numpy() for _, labels in ds])
    y_pred = np.argmax(model.predict(ds, verbose=0), axis=1)
    matrix = tf.math.confusion_matrix(y_true, y_pred, num_classes=len(CLASS_NAMES)).numpy()

    print("\nMatriz de confusión (filas = real, columnas = predicción):")
    print(" " * 10 + "".join(f"{name:>10}" for name in CLASS_NAMES))
    for name, row in zip(CLASS_NAMES, matrix):
        print(f"{name:>10}" + "".join(f"{v:>10}" for v in row))


if __name__ == "__main__":
    train_ds, val_ds, test_ds = load_datasets()
    train_ds = prepare(train_ds, shuffle=True)
    val_ds = prepare(val_ds)
    test_ds = prepare(test_ds)

    model = build_model()
    model.summary()

    callbacks = [
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3),
    ]
    history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks, verbose=2)

    plot_history(history)

    test_loss, test_acc = model.evaluate(test_ds, verbose=0)
    print(f"\nTest loss: {test_loss:.4f}  |  Test accuracy: {test_acc:.4f}")
    confusion_matrix(model, test_ds)

    model.save(OUTPUT_PATH / "rps_cnn.keras")
    model.save_weights(OUTPUT_PATH / "rps_cnn.weights.h5")
    print(f"\nModelo guardado en {OUTPUT_PATH / 'rps_cnn.keras'}")
    print(f"Pesos guardados en {OUTPUT_PATH / 'rps_cnn.weights.h5'}")
