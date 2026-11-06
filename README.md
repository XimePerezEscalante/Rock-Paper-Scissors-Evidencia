# **Rock-Paper-Scissors-Evidencia**

CNN programada usando el framework TensorFlow/Keras que clasifica fotografías de una mano como **piedra**, **papel** o **tijeras**, junto con una aplicación web desarrollada en Next.js donde puedes subir una fotografía y el modelo juega el movimiento que vence al tuyo.

## **Dataset**
Se obtuvo de la plataforma Kaggle del siguiente link: https://www.kaggle.com/datasets/alexandredj/rock-paper-scissors-dataset

El proyecto consta de dos partes que se ejecutan simultáneamente:

| Parte | Función | Se ejecuta en |
|---|---|---|
| `serve.py` (Python, FastAPI) | Carga el modelo entrenado (`rps_cnn.keras`) y responde a las solicitudes de predicción. | http://127.0.0.1:8000 |
| `rockpaperscissors-app/` (Next.js) | Página web para subir imágenes y visualizar los resultados. | http://localhost:3000 |

El modelo entrenado ya está incluido, por lo que **no necesitas entrenar nada para ejecutar la aplicación**.

## **Requisitos**

- **Python 3.10 – 3.12** TensorFlow todavía no es compatible con Python 3.14.
- **Node.js 20 o superior** y npm.

## **1. Configurar el entorno de Python (sólo una vez)**

Desde la carpeta raíz del repositorio:

```bash
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

> En Windows, utiliza `.venv\Scripts\pip` y `.venv\Scripts\python` en lugar de `.venv/bin/...`.

## **2. Iniciar el servidor del modelo**

En una terminal, desde la carpeta raíz del repositorio, ejecuta:

```bash
.venv/bin/uvicorn serve:app --port 8000
```

Espera hasta que aparezca el mensaje `Application startup complete` (la carga de TensorFlow tarda algunos segundos).

Para comprobar que funciona, abre [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health). Debería mostrar una respuesta similar a:

```json
{"status":"ok", ...}
```

Deja esta terminal abierta.

## **3. Iniciar la aplicación web**

En una segunda terminal, ejecuta:

```bash
cd rockpaperscissors-app
npm install
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000), sube una fotografía de tu mano (JPG, PNG o WEBP) y haz clic en **Analizar imagen**.

La tabla de resultados muestra el movimiento predicho, el nivel de confianza de la predicción y el movimiento que realiza el modelo para vencerte.

Si el servidor del modelo no está en funcionamiento, la página mostrará el error *"No se pudo conectar con el servidor del modelo"*. Regresa al paso 2.

Si el servidor del modelo se ejecuta en otra dirección, crea el archivo `rockpaperscissors-app/.env.local` con el siguiente contenido:

```env
MODEL_URL=http://127.0.0.1:8000/predict
```

## **Utilizar el modelo desde la terminal (opcional)**

Puedes clasificar una o varias imágenes sin utilizar la aplicación web:

```bash
.venv/bin/python predict.py path/to/photo1.jpg path/to/photo2.png
```

Ejemplo de resultado:

```text
photo1.jpg -> rock   (rock: 89.37%  paper: 7.81%  scissors: 2.82%)
```

## **Volver a entrenar o evaluar el modelo (opcional)**

Estos procedimientos requieren el conjunto de datos de imágenes, el cual **no está incluido en el repositorio**.

Colócalo dentro de una carpeta llamada `images/` en la raíz del proyecto, con una carpeta para cada categoría que contenga imágenes PNG:

```text
images/
  rock/       *.png
  paper/      *.png
  scissors/   *.png
```

**Evaluar el modelo:** evalúa el modelo incluido utilizando el conjunto de prueba (muestra la precisión y la matriz de confusión):

```bash
.venv/bin/python predict.py
```

**Volver a entrenar el modelo:** sobrescribe los archivos `rps_cnn.keras` y `rps_cnn.weights.h5`, y guarda el archivo `training_history.png`:

```bash
.venv/bin/python train_cnn.py
```

A velocidad normal, el entrenamiento tarda aproximadamente entre 20 y 25 minutos en una computadora portátil utilizando la CPU. Sin embargo, si la computadora entra en reposo, el proceso puede extenderse durante varias horas.

## **Archivos del proyecto**

| Archivo | Descripción |
|---|---|
| `preprocess.py` | Carga las imágenes, les asigna etiquetas (rock = 0, paper = 1, scissors = 2), normaliza sus valores al rango de 0 a 1 y divide los datos en conjuntos de entrenamiento, validación y prueba en proporciones de 70 / 15 / 15, utilizando una semilla fija. |
| `train_cnn.py` | Define la red neuronal convolucional (aumento de datos + 4 bloques convolucionales), la entrena y guarda el modelo. |
| `predict.py` | Carga el modelo entrenado para evaluarlo o clasificar imágenes individuales. |
| `serve.py` | Servidor FastAPI utilizado por la aplicación web (`POST /predict`, `GET /health`). |
| `rps_cnn.keras` | Modelo entrenado (arquitectura + pesos). |
| `rps_cnn.weights.h5` | Contiene únicamente los pesos. Se carga utilizando `build_model()` + `model.load_weights(...)`. |
| `requirements.txt` | Dependencias de Python. |
| `rockpaperscissors-app/` | Aplicación web desarrollada en Next.js (consulta su propio archivo `README.md`). |
| `Paper_IA_RockPaperScissors.pdf` | Reporte del proyecto. |

## **Resultados**

El modelo incluido alcanza una **precisión del 75.9 %** en el conjunto de prueba (407 imágenes).

Reconoce correctamente las categorías de piedra y papel (aproximadamente un 94 % en cada una), pero suele confundir las tijeras con el papel.

Las fotografías con un fondo claro y uniforme, similares a las imágenes utilizadas durante el entrenamiento, ofrecen los mejores resultados.
